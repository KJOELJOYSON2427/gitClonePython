from Repository import Repository
from Tree import Tree
from commit import Commit


class Status:

    def __init__(self, repo:Repository):
      self.repo = repo
      
    def status(self):
        """Git’s Status Logic

Untracked files: present in working directory, not in index, not in last commit.

Changes not staged for commit: working directory differs from index.

Changes to be committed: index differs from last commit.

Clean: everything matches HEAD.
        """
        # what branch we are on 
        current_branch = self.repo.get_current_branch()
        print(f"On branch {current_branch if current_branch else '(detached HEAD)'}")
        index =self.repo.load_index() #current index
       
        commit_hash = self.repo.get_branch_commit(current_branch)
        #previous commit ->index build

        """
        Compare the previous and current index
        """
        last_index_files={}
        if commit_hash:
            try:
                commit_object=self.repo.load_object(commit_hash)
                commit=Commit.from_content(commit_object)

                if commit.tree_hash:
                    last_index_files=self.build_index_from_tree(commit.tree_hash)
                    #let us compare and find the new if there is a staged change
                    
            except:    
                last_index_files={}
       
        # added = index.keys() - last_index_files.keys()
        for file_path in set(index.keys()) | set(last_index_files.keys()):
            index_hash = index.get(file_path)
            last_hash = last_index_files.get(file_path)

            if last_hash is None and index_hash is not None:
              print(f"        new file:   {file_path}")
            if  index_hash and last_hash and last_hash != index_hash:
                print(f"        modified:   {file_path}")


        #what files are stagged for commit ->index
        #what files have modified but not staged
        #what files are untracked
        #what files have been delete
        pass  



    def build_index_from_tree(self, tree_hash: str) -> dict:
        """
        Given a tree hash, reconstruct the index (path → blob_hash).
        """
        index = {}
        def walk_tree(tree_hash: str, prefix: str=""):
           tree_obj = self.repo.load_object(tree_hash)
           tree = Tree.from_content(tree_obj.content)

           for mode,name, obj_hash in tree.entries:
               path = f"{prefix}//{name}" if prefix else name
               if mode.startswith("400"):  # directory
                   walk_tree(obj_hash, path)
               elif mode.startswith("100"):  # blob (file)
                  index[path] = obj_hash

        walk_tree(tree_hash)
        return index
