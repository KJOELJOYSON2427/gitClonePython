import time
from typing import List
from GitObject import GitObject


class Commit(GitObject):
    def __init__(self,  
                 tree_hash: str,
                 commit_message: str, 
                 author_name: str, 
                 committer: str,
                 parent_hashes: List[str],
                 timestamp: int = None):
        """
        Initialize a commit object.
        """
        self.tree_hash = tree_hash
        self.parent_hashes = parent_hashes
        self.author = author_name
        self.timestamp = timestamp or int(time.time())
        self.committer = committer
        self.commit_message = commit_message

        # Serialize and pass content to GitObject
        content = self._serialize_commit()
        super().__init__("commit", content)

    @property
    def message(self) -> str:
        return self.commit_message          

    def _serialize_commit(self) -> bytes:
        """
        Convert commit attributes to bytes content.
        """
        lines = [f"tree {self.tree_hash}"]

        for parent in self.parent_hashes:
            lines.append(f"parent {parent}")

        # Author and committer
        lines.append(f"author {self.author} {self.timestamp} +0000")
        lines.append(f"committer {self.committer}")

        # Blank line before message
        lines.append("")
        lines.append(self.commit_message)

        return "\n".join(lines).encode()

    @classmethod
    def from_content(cls, content: bytes):
        """
        Reconstruct a Commit object from serialized content.
        """
        lines = content.decode().split("\n")
        tree_hash = None
        author = None
        parent_hashes = []
        committer = None
        timestamp = 0
        message_start = 0

        for i, line in enumerate(lines):
            if line.startswith("tree "):
                tree_hash = line[5:]
            elif line.startswith("parent "):
                parent_hashes.append(line[7:])
            elif line.startswith("author "):
                # Handle author + timestamp + timezone
                parts = line[7:].rsplit(" ", 2)
                author = parts[0]
                timestamp = int(parts[1])
            elif line.startswith("committer "):
                committer = line[10:]
            elif line.strip() == "":
                message_start = i + 1

        message = "\n".join(lines[message_start:]).strip()

        return cls(tree_hash, message, author, committer, parent_hashes, timestamp)
