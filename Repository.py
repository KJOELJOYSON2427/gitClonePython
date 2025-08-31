import json
from pathlib import Path
from typing import Dict
from GitObject import GitObject
from Blob import Blob  
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
          if not full_path.exists() or not full_path.is_file():
               raise FileNotFoundError(f"File {full_path} does not exist.")
          
          #Read the file content
          content = full_path.read_bytes()
          # Create BLOB object from the content which is a class
          blob = Blob(content)
          # store the blob object in database (.pygit/objects)
          blob_hash =self.store_object(blob)
          #Update index to include the file 
          index=self.load_index()

          index[path]=blob_hash

          self.save_index(index)
          print(f"Added file {path} to staging area.")



     def add_directory(self,path:str)->None:
          pass

     def store_object(self, obj:GitObject)->str:
          object_hash=obj.hash()
          object_dir= self.objects_dir / object_hash[:2]
          object_file = object_dir /object_hash[2:]

          if not object_dir.exists():
               object_dir.mkdir(exist_ok=True)
          if not object_file.exists():
               object_file.write_bytes(obj.serialize())

          return object_hash 

     def load_index(self)->Dict[str, str]:
          if not self.index_file.exists():
               return {}
          try:
               return json.loads(self.index_file.read_text())
          except:
               return {}    



     def save_index(self, index:Dict[str,str])->None:
          self.index_file.write_text(json.dumps(index,indent=2))