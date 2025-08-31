

import hashlib
import zlib


class GitObject:
    def __init__(self, obj_type: str, content:bytes):
        self.type=obj_type
        self.content=content


    def hash(self)->str:
        #<type><size>/0<content>
        header=f"{self.type} {self.content.__len__()}\0".encode()
        full_content=header+self.content
        return hashlib.sha256(full_content).hexdigest()    
    

    def serialize(self)-> bytes:
        header=f"{self.type} {self.content.__len__()}\0".encode()
        return zlib.compress(header+self.content)
    
    @classmethod
    def deserialize(cls,data:bytes)-> "GitObject":
        decompressed_data =zlib.decompress(data)
        find_index=decompressed_data.find(b"\0")
        header =decompressed_data[:find_index]
        content=decompressed_data[find_index+1:]

        object_type, _=header.split(" ")

        return cls(object_type.decode(), content)