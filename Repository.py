import json
from pathlib import Path
from typing import Dict
from GitObject import GitObject
from Blob import Blob  
from Tree import Tree  
from commit import Commit

class Repository:

     def __init__(self, path="."):
          
          self.path =Path(path).resolve()
          self.get_dir = self.path / ".pygit"

          self.objects_dir = self.get_dir / "objects"
          self.refs_dir = self.get_dir / "refs"
          self.heads_dir = self.refs_dir/ "heads"
          self.head_file = self.get_dir / "HEAD"

          self.index_file = self.get_dir/ "index"

     def init(self)->bool:
          
          if self.get_dir.exists():
               print(f"Repository is intialized in  {self.get_dir}")
               return False
          # create the file with the current initialization
          self.get_dir.mkdir() 
          self.objects_dir.mkdir()
          self.refs_dir.mkdir()
          self.heads_dir.mkdir()   

          # creating intial head pointing to a branch  
          self.head_file.write_text("ref: refs/heads/master\n")

          self.save_index({})

          print(f"Initialized empty Pygit repository in {self.get_dir}")

          return True
     

     def add(self,path:str)-> None:

          abs_path =self.path / path
          if not abs_path.exists():
               raise FileNotFoundError(f"Path {abs_path} does not exist.")
          
          if abs_path.is_dir():
               self.add_directory(path)
          elif abs_path.is_file():
               self.add_file(path)     
     

     def add_file(self, path:str)-> None:
          full_path =self.path / path
          print(full_path)
          if not full_path.exists() or not full_path.is_file():
               raise FileNotFoundError(f"File {full_path} does not exist.")
          
          #Read the file content
          content = full_path.read_bytes()
          # Create BLOB object from the content which is a class
          blob = Blob(content)
          # store the blob object in database (.pygit/objects)
          print("came 6")
          blob_hash =self.store_object(blob)
          #Update index to include the file 
          print("came 6")
          index=self.load_index()

          index[path]=blob_hash

          self.save_index(index)
          print("came 6")
          # Safe point to call garbage collection
          
          print(f"Added file {path} to staging area.")



     def add_directory(self, path: str, added_count=0) -> int:
           print(f"Adding directory: {path}")
           full_path = self.path / path
           print(full_path)
           if not full_path.exists():
              print("came 1")
              raise FileNotFoundError(f"Directory {full_path} does not exist.")
           if not full_path.is_dir():
              print("came 2")
              raise NotADirectoryError(f"Path {full_path} is not a directory.")

           for item in full_path.iterdir():
               print("came 3")
               rel_path = item.relative_to(self.path)
               print(rel_path)
           # Skip git internals
               if rel_path.parts[0] in [".pygit", ".git", "__pycache__"] or item.is_symlink():
                  print("came 4")
                  continue
               if item.is_file():
                   print("came 5")
                   print(item.relative_to(self.path))
                   self.add_file(str(item.relative_to(self.path)))
                   added_count += 1
                   print(added_count)
               elif item.is_dir():
                   added_count = self.add_directory(str(item.relative_to(self.path)), added_count)

           if added_count > 0:
               print(f"Added {added_count} files from directory: {full_path}")
           else:
               print(f"No files added from directory: {full_path}")

     def store_object(self, obj:GitObject)->str:
          object_hash=obj.hash()
          object_dir= self.objects_dir / object_hash[:2]
          object_file = object_dir /object_hash[2:]
          print("came 7")
          if not object_dir.exists():
               print("came 8")
               object_dir.mkdir(parents=True, exist_ok=True)
               print("came 9")
          if not object_file.exists():
               object_file.write_bytes(obj.serialize()) #here it is serialized

          return object_hash 

     def load_index(self)->Dict[str, str]:
          if not self.index_file.exists():
               return {}
          try:
               return json.loads(self.index_file.read_text())
          except:
               return {}    

     def load_object(self, object_hash: str) -> GitObject:
          print("came 11")
          object_dir = self.objects_dir / object_hash[:2]
          object_file = object_dir / object_hash[2:]
          if not object_file.exists():
              raise FileNotFoundError(f"Object {object_hash} not found")
          data = object_file.read_bytes()
          return GitObject.deserialize(data) # i dont think this will work
           
     
     def save_index(self, index:Dict[str,str])->None:
          self.index_file.write_text(json.dumps(index,indent=2))


     def garbage_collect(self):
          index = self.load_index()
          used_hashes=set(index.values())


          for folder in self.objects_dir.iterdir():
               if folder.is_dir():
                    for obj_file in folder.iterdir():
                         full_hash = folder.name + obj_file.name
                         if full_hash not in used_hashes:
                              obj_file.unlink()
                              print(f"Removed unreferenced object {full_hash}")
                         #Remove folder if empty
                         if not any(folder.iterdir()):
                              folder.rmdir() 


     def commit(
               self,
               message:str,
               committer:str,
               author:str="Pygit user at <email@email.com>"
                )->None| str:
          #create a tree object from the index (staging area and stored it in objects)
          tree_hash= self.create_tree_from_index() #root hash


          current_branch=self.get_current_branch()
          print(current_branch)
          print("came10")
          parent_commit = self.get_branch_commit(current_branch=current_branch)

          index = self.load_index()
          if not index:
               print("nothing to commit, working tree clean")
               return None

          # ✅ check if tree is same as parent's tree
          if parent_commit is not None:
                parent_obj_git_commit = self.load_object(parent_commit)
                parent_obj=Commit.from_content(parent_obj_git_commit.content)   # load commit object
                if tree_hash == parent_obj.tree_hash:
                    print("nothing to commit, working tree clean")
                    return None
          parent_hashes= [parent_commit] if parent_commit != None else [] #ternary operator
          
          

          commit= Commit(
               tree_hash=tree_hash,
               author_name=author,
               committer=committer or author,
               commit_message=message,
               parent_hashes=parent_hashes,   # parent comes from head
          )
          commit_hash = self.store_object(commit)
          #clean the index 
          self.save_index({})
          self.set_branch_commit(current_branch, commit_hash) # for the ref/heads/file commit creation
          print(f"Created the commit {commit_hash} in branch {current_branch}")
          return commit_hash





     def get_branch_commit(self, current_branch: str)-> str | None:
          branch_file = self.heads_dir / current_branch
          if branch_file.exists():
               return branch_file.read_text().strip()
          
          return None
     

     def get_current_branch(self)->str:
          if not self.head_file.exists():
               return "master"
          
          head_content = self.head_file.read_text().strip()
          print(head_content)
          print(head_content.startswith("refs: ref/heads/"))
          if head_content.startswith("refs: ref/heads/"):    
               return head_content[16:]
          
          return "HEAD" #detatched head due to checkout



     def create_recursive_tree_object(self,entries:Dict)->str:
          tree=Tree()

          for name,blob_hashOrFolderNested in entries.items():
               if isinstance(blob_hashOrFolderNested, str):
                    tree.add_entry("100644",name, blob_hashOrFolderNested)

               if isinstance(blob_hashOrFolderNested,dict):
                    subtree_hash=self.create_recursive_tree_object(blob_hashOrFolderNested)
                    tree.add_entry("40000", name, subtree_hash)

          return self.store_object(tree)                
     


     #it create s a dict then a tree object to the createrecursive tree ->root hash
     def create_tree_from_index(self)->str:
          index =self.load_index()

          if not index:
               tree=Tree()
               return self.store_object(tree)
          
          dirs={}
          files={}

          for file_path, blob_hash in index.items():
               parts=file_path.split("//")


               if len(parts)==1:
                    #file in root
                    files[parts[0]]=blob_hash
               else: 
                    dirs_name = parts[0]
                    if dirs_name not in dirs:
                         dirs[dirs_name]={}

                    current=dirs[dirs_name]
                    for part in parts[1:-1]:
                         if part not in current:
                          # dictionary value reference
                            current[part]={}         
                         current=current[part]

                    current[parts[-1]]=blob_hash  

          root_entries={**files}  #root files
          for dict_name,dict_contents in dirs.items():
               root_entries[dict_name]=dict_contents


          return self.create_recursive_tree_object(root_entries)


     def set_branch_commit(self , current_branch: str, commit_hash:str):
          branch_file = self.heads_dir / current_branch

          if not branch_file.exists():
               branch_file.write_text(commit_hash)

          branch_file.write_text(commit_hash + "\n")     




  
