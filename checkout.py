from pathlib import Path
from Repository import Repository
from Tree import Tree
from commit import Commit
from Blob import Blob


class CheckoutError(Exception):
    pass


class Checkout:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_files_from_tree_recursive(self, tree_hash: str, prefix: str = "") -> set[str]:
        """Recursively collect all file paths from a tree object."""
        files = set()
        try:
            tree_obj = self.repo.load_object(tree_hash)
            tree = Tree.from_content(tree_obj.content)

            for mode, name, obj_hash in tree.entries:
                full_path = f"{prefix}{name}"
                if mode.startswith("100"):  # file
                    files.add(full_path)
                elif mode.startswith("400"):  # directory
                    nested_files = self.get_files_from_tree_recursive(
                        obj_hash, prefix=full_path + "/"
                    )
                    files.update(nested_files)

        except Exception as e:
            print(f"Warning: could not read tree {tree_hash}: {e}")

        return files

    def restore_tree(self, tree_hash: str, path: Path):
        """Restore a tree (recursively) into the working directory."""
        tree_obj = self.repo.load_object(tree_hash)
        tree = Tree.from_content(tree_obj.content)

        for mode, name, obj_hash in tree.entries:
            file_path = path / name
            if mode.startswith("100"):  # blob (file)
                blob_obj = self.repo.load_object(obj_hash)
                blob = Blob(blob_obj.content)
                file_path.write_bytes(blob.content)
            elif mode.startswith("400"):  # subtree (directory)
                file_path.mkdir(exist_ok=True)
                self.restore_tree(obj_hash, file_path)



    def restore_working_directory(self, branch: str, files_to_clear: set[str]):
        """Clear old files and restore the tree from target branch."""
        target_commit_hash = self.repo.get_branch_commit(branch)
        if not target_commit_hash:
            return

        # Step 1: remove files tracked by previous branch
        for rel_path in sorted(files_to_clear):
            file_path = self.repo.path / rel_path
            try:
                if file_path.is_file():
                    file_path.unlink()
                # optional: remove empty dirs
                elif file_path.is_dir() and not any(file_path.iterdir()):
                    file_path.rmdir()
            except Exception:
                pass

        # Step 2: restore files from target commit
        target_commit_obj = self.repo.load_object(target_commit_hash)
        target_commit = Commit.from_content(target_commit_obj.content)

        if target_commit.tree_hash:
            self.restore_tree(target_commit.tree_hash, self.repo.path)




    def checkout(self, branch: str, create_branch: bool):
        """Switch branches, optionally creating a new one."""
        # Step 1: Check index for staged changes
        index = self.repo.load_index()
        if index:
            raise CheckoutError(
                "Cannot switch branch: you have staged changes. Commit or reset first."
            )

        # Step 2: compute files to clear from previous branch
        previous_branch = self.repo.get_current_branch()
        files_to_clear = set()
        previous_commit_hash = None
        try:
            previous_commit_hash = self.repo.get_branch_commit(previous_branch)
            if previous_commit_hash:
                prev_commit_obj = self.repo.load_object(previous_commit_hash)
                prev_commit = Commit.from_content(prev_commit_obj.content)
                if prev_commit.tree_hash:
                    files_to_clear = self.get_files_from_tree_recursive(prev_commit.tree_hash)
        except Exception:
            files_to_clear = set()

        # Step 3: branch creation / switching
        branch_file = self.repo.heads_dir / branch
        if not branch_file.exists():
            if create_branch:
                if previous_commit_hash:
                    self.repo.set_branch_commit(branch, previous_commit_hash)
                    print(f"Created new branch {branch}")
                else:
                    print("No commits yet, cannot create a branch")
                    return
            else:
                print(f"Branch '{branch}' not found.")
                print(
                    f"Use 'python3 main.py checkout -b {branch}' to create and switch to a new branch."
                )
                return

        # Step 4: move HEAD to new branch
        self.repo.head_file.write_text(f"ref: refs/heads/{branch}\n")

        # Step 5: restore working directory
        self.restore_working_directory(branch, files_to_clear)

        print(f"Switched to branch {branch}")
