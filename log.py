import time
from Repository import Repository
from commit import Commit


class Log:
    def __init__(self,repo:Repository):
        self.repo = repo

    def log(self, max_count: int =10):
        current_branch = self.repo.get_current_branch()
        if not current_branch:
            print("Detached HEAD or no branch found.")
            return
        commit_hash = self.repo.get_branch_commit(current_branch)
        if not commit_hash:
            print("there is no commit yet ")
            return
        else:
            count =0 
            while commit_hash and count < max_count: #parent commit should be there
                commit_obj = self.repo.load_object(commit_hash)
                commit=Commit.from_content(commit_obj.content)
                
                # Print commit info
                print(f"commit {commit_hash}")
                print(f"Author: {commit.author}")
                print(f"Date:   {time.strftime('%c', time.localtime(commit.timestamp))}\n")
                print(f"    {commit.message}\n")

                count+=1
                
                if commit.parent_hashes:        # parent_hashes is a list, take the first
                  commit_hash = commit.parent_hashes[0] if len(commit.parent_hashes[0]) < 2 else None
                else:
                   commit_hash = None          # reached the first commit


             



