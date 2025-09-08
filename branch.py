from Repository import Repository
from abc import ABC, abstractmethod
from commit import Commit
from typing import List


class BranchInterface(ABC):
    @abstractmethod
    def create(self, name: str) -> None:
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        pass

    @abstractmethod
    def list(self) -> List[str]:
        pass


class Branch(BranchInterface):

    def __init__(self, repo: Repository):
        self.repo = repo

    def create(self, branch_name: str):
        """Create a new branch at the current HEAD commit."""
        if not branch_name:
            raise ValueError("Branch name is required")

        branch_file = self.repo.heads_dir / branch_name
        if branch_file.exists():
            print(f"Branch '{branch_name}' already exists.")
            return

        # Get current HEAD commit hash
        head_ref = self.repo.head_file.read_text().strip()
        if head_ref.startswith("ref:"):
            ref_path = self.repo.get_dir / head_ref.split(" ")[1]
            if not ref_path.exists():
                print("No commits yet, cannot create branch.")
                return
            commit_hash = ref_path.read_text().strip()
        else:
            # Detached HEAD
            commit_hash = head_ref

        if not commit_hash:
            print("No commits yet, cannot create branch.")
            return

        branch_file.write_text(commit_hash)
        print(f"Branch '{branch_name}' created at commit {commit_hash[:7]}")

    def delete(self, branch_name: str):
        if not branch_name:
            raise ValueError("Branch name is required")

        branch_file = self.repo.heads_dir / branch_name
        if branch_file.exists():
            branch_file.unlink()
            print(f"Deleted branch '{branch_name}'")
        else:
            print(f"Branch '{branch_name}' not found")

    def list(self) -> List[str]:
        branches = []
        current_branch = self.repo.get_current_branch()
        
        head_ref = self.repo.head_file.read_text().strip()
        
        
        if self.repo.heads_dir.exists():
            for branch_file in sorted(self.repo.heads_dir.iterdir()):
      
                if branch_file.is_file():

                    branch_name = branch_file.name
                    commit_hash = branch_file.read_text().strip()
                    
                    # Load commit message
                    message = "?"
                    try:
                        commit_obj = self.repo.load_object(commit_hash)
                        
                        commit = Commit.from_content(commit_obj.content)
                        
                        message = commit.message.splitlines()[0]
                        
                    except Exception:
                        pass

                    # Mark current branch
                    if branch_name == current_branch:
                        branches.append(f"* {branch_name} ({commit_hash[:7]}) {message}")
                        print("came")
                    else:
                        branches.append(f"  {branch_name} ({commit_hash[:7]}) {message}")

        # Handle detached HEAD
        if current_branch is None and not head_ref.startswith("ref:"):
            print("came112")
            commit_hash = head_ref
            message = "?"
            try:
                commit_obj = self.repo.load_object(commit_hash)
                commit = Commit.from_content(commit_obj.content)
                message = commit.commit_message.splitlines()[0]
            except Exception:
                pass
            branches.append(f"* (detached HEAD at {commit_hash[:7]}) {message}")
            

        print(branches)    
        return branches
