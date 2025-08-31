from GitObject import GitObject

class Blob(GitObject):

    def __init__(self, content: bytes):
        super().__init__("blob", content)
        
    def get_content(self)->bytes:
        return self.content   

