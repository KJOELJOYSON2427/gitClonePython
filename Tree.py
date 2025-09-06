from typing import List, Tuple
from GitObject import GitObject
class Tree(GitObject):
                               #<mode> <name>\0<hash> ->directory or bhb hassh
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

    
    @classmethod
    def from_content(cls, content: bytes)->"Tree":
        tree =cls()
        i=0 # index it
        hash_len = 32  # bytes for SHA-256 (20 for SHA-1)
        while i<len(content):
            nullidx= content.find(b"\0",i)
            
            if nullidx == -1:
                break
            mode_and_name = content[i:nullidx].decode()
            mode,name=mode_and_name.split(" ",1)
            start = nullidx + 1
            end = start + hash_len
            object_hash = content[start:end].hex()
            tree.entries.append((mode,name,object_hash))

            #increment the i pointer
            i=i+end

        return tree    



