import time
from typing import List
from GitObject import GitObject



class Commit(GitObject):
    def __init__(self,  
                 tree_hash:str,
                 commit_message:str, 
                 author_name:str, 
                
                 committer:str,
                 parent_hashes: List[str],
                 timestamp:int = None,
           
                 ):
        #serialize before  pass the content i9n bytes
        self.tree_hash=tree_hash
        self.parent_hashes=parent_hashes
        self.author =author_name
        self.timestamp=timestamp or int(time.time())
        self.committer=committer
        self.commit_message=commit_message

        content = self._serialize_commit()
        super().__init__("commit", content)
              

    def _serialize_commit(self):
        lines = [f"tree {self.tree_hash}"]

        for parent in self.parent_hashes:
           lines.append(f"parent {parent}")

        # Author and committer (for realism, you can use same values)
        lines.append(f"author {self.author} {self.timestamp} +0000")
        lines.append(f"committer {self.author}")

        # Blank line before message
        lines.append("")
        lines.append(self.commit_message)

        return "\n".join(lines).encode()
    
    @classmethod
    def from_content(cls, content:bytes):
        lines = content.decode()
        lines=lines.split("\n")
        tree_hash = None
        author=None
        _parent_hashes=[]
        committer=None
        message_start= 0
        timestamp=0

        for i, line in enumerate(lines):
            if line.startswith("tree "):
                tree_hash=line[5:]
            elif line.startswith("parent "):
                _parent_hashes.append(line[7:])
            elif line.startswith("author: "):
                author_parts=line[7:].rsplit(" ", 2) 
                author = author_parts[0]
                timestamp=int(author_parts[1])
            elif line.startswith("committer: "):
                committer_parts=line[10:].rsplit(" ", 2) 
                committer = committer_parts[0]

            elif line =="":
                message_start = i+1 # index+1 next list item
                break;    
        
        message = "\n".join(lines[message_start+1:])
        commit = cls(tree_hash, message,author,committer, _parent_hashes,timestamp)
        return commit

   
          