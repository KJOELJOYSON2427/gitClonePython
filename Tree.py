from typing import List, Tuple
from GitObject import GitObject
class Tree(GitObject):

    def __init__(self, entries: List[Tuple[str, str,str]]=None):
        self.entries=entries or []
        content = self._serialize_entries()
        super().__init__("tree", content)


     # called through add_entry for bytes conversion of the 
    def _serialize_entries(self)-> bytes:
        #<mode> <name>\0<hash>
        content = b""
        for mode, name , obj_hash in  sorted(self.entries):
            content+=f"{mode} {name}\0".encode()
            content+= bytes.fromhex(obj_hash)

        return content
    
   
    def add_entry(self,mode:str, name:str, blob_hashOrSubTreeHash:str):
        # needed during hash time 
        self.entries.append((mode,name,blob_hashOrSubTreeHash))
        self.content=self._serialize_entries()
        

