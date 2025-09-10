from pathlib import Path
from typing import Dict, List
from Blob import Blob
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
        #what files are stagged for commit ->index
        stagged_files:list[tuple]=[]
        for file_path in set(index.keys()) | set(last_index_files.keys()):
            index_hash = index.get(file_path)
            last_hash = last_index_files.get(file_path)

            if index_hash and not last_hash:
              stagged_files.append(("new file", file_path))
            #   print(f"        new file:   {file_path}")
            if  index_hash and last_hash and last_hash != index_hash:
                stagged_files.append(("modified ", file_path))
                # print(f"        modified:   {file_path}")

        if stagged_files:
             print("\nChanged to be committed:")
             for (stagged_status, file_path) in sorted(stagged_files):
               print(f"       {stagged_status}:  {file_path}")
        
        #what files have modified but not staged -> once commited in but in current working directory it is changed but not staged
        unstaged_files=[]
        print("log1")
        working_dirs_files=self.get_working_directory()
        for file_path in working_dirs_files:
            if file_path in index:
                if working_dirs_files[file_path] !=working_dirs_files[file_path]:
                    unstaged_files.add(file_path)
        if unstaged_files:
             print("\nChanges not staged for commit:\n   use \"git add <file>...\" to update what will be committed\n    use \"git restore <file>...\" to discard changes in working directory")
             for  file_path in sorted(unstaged_files):
               print(f"      modified: {file_path}")            
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
    


#             [
#         PosixPath('repo/main.py'),
#     PosixPath('repo/utils/helper.py'),
#     PosixPath('repo/utils/nested/deep_file.py'),
#     PosixPath('repo/data/sample.txt')
# ]
            
    def get_all_files(self)->List[Path]:
        files =[]

        for item in self.repo.path.rglob("*"):
            if [".git", "__pycache__"] in item.parts:
                continue

            if item.is_file():
                files.append(item)
        return files          

    #figure out all the  files present within the working directory
    #dictionary mapping
    def get_working_directory(self)->Dict[str,str]:
        working_dir_files:Dict[str,str]={}
        files_of_dir:List[Path]=self.get_all_files()
        for item in files_of_dir:
            rel_path=str(item.relative_to(self.repo.path))
            
            try:
                content = item.read_bytes()
                blob =Blob(content)
                working_dir_files[rel_path]=blob.hash() # *init called the content
                
            except Exception:
                continue
        print("log2")    
        return working_dir_files    
