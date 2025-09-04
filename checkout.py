from Repository import Repository

class Checkout():

    def __init__(self, repo: Repository):
        self.repo = repo
    


    def get_files_from_recursive(self, tree_hash:str):
        files=set()

        try:
          pass
        except Exception as e:
          print(f"Warning: could not read tree {tree_hash}")      


    def checkout(self, branch:str, create_branch: bool):

        branch_file = self.repo.heads_dir / branch
        if not branch_file.exists():
            if create_branch:
                current_branch  = self.repo.get_current_branch()
                current_commit=self.repo.get_branch_commit(current_branch) #commit_hash is there there is a chance no commit yet
                #maybe they made the checkout before even commit so  u have tto stage and commit first
                if current_commit:
                    self.repo.set_branch_commit(branch,current_commit)
                    print(f"Created new branch {branch} with heads have this and head pointing to it.")

                else:
                    print("No commit yet, cannot create a branch named {branch}.")
                    #later we will create a support for this 
                    # or use this
                    #branch_file.write_text("")
                    # self.set_head_file(branch_file)
                    #  print(f"Created new branch {branch} with heads have this and head pointing to it as unborn commit")   
                    return
            else:
               print(f"Branch '{branch}' not found.")
               print(
                "Use 'python3 pygit.py checkout -b {branch}' to create and switch the new branch"
            )
        self.set_head_file(branch)   #this when we have the  branch andkeep by overiding the head when we create it or we may get it the commit in it to the branch  
        print(f"Switched to branch {branch}")           
                   

        

    def set_head_file(self, branch_name_to_ref:str):
        self.repo.head_file.write_text(f"refs: ref/heads/{branch_name_to_ref}\n")

