import json
from pathlib import Path


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

          self.index_file.write_text(json.dumps({},indent = 2))

          print(f"Initialized empty Pygit repository in {self.get_dir}")

          return True
     

     def add(self,path:str)-> None:

          abs_path =self.path / path
          if not abs_path.exists():
               raise FileNotFoundError(f"Path {abs_path} does not exist.")
          
          if abs_path.is_dir():
               self.add_directory(abs_path)
          elif abs_path.is_file():
               self.add_file(abs_path)     
     

     def add_file(self, path:Path)-> None:
          