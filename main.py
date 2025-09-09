import argparse
from pathlib import Path
import sys
from Repository import Repository

# parser= argparse.ArgumentParser(
#     description="A Git for wonderland joy"
# )

# parser.add_argument(
#     "repository",
#     help="Path to the repository"
# )

# subParsers = parser.add_subparsers(
#     dest="command"
# )


# parser_add=subParsers.add_parser(
#     "add",
#     help="Add something"
# )
# parser_add.add_argument("x", type=int, help="First number")
# parser_add.add_argument("y", type=int, help="Second number")

# parser_sub = subParsers.add_parser("subtract", help="Subtract something")


# parser_sub.add_argument("x", type=int, help="First number")
# parser_sub.add_argument("y", type=int, help="Second number")


# args = parser.parse_args()

# print(args)
# if args.command == "add":
#     print(args.x+args.y)
# elif args.command == "subtract":
#     print(args.x-args.y)



# git state maintenance
from Status import Status
from branch import Branch
import argparse
import sys
from checkout import Checkout
from log import Log


def create_parser():
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        description="Python - A simple git CLI"
    )
    return parser


def add_subparsers(parser):
    """Add subparsers and return them."""
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available Commands"
    )

    # init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new Git Repository"
    )

    


    # add command
    add_parser =subparsers.add_parser(
        "add",
        help="Add files and directories to the staging area"
    )
    add_parser.add_argument(
        "paths",
        nargs="+",
        help="Files and directories to add"
    )

    #commit parser
    commit_parser=subparsers.add_parser(
        "commit", help="Commit changes to the repository"
    )


    commit_parser.add_argument(
        "-m",
        "--message",
        help="Commit message",
        required=True
    )
    commit_parser.add_argument(
        
        "--author",
        help="Author of the commit",
        
    )
    commit_parser.add_argument(
        
        "--committer",
        help="committer of the commit",
        
    )
    #checkout command
    checkout_parser = subparsers.add_parser(
        "checkout",
        help="Move/Create a new branch"
    )
    checkout_parser.add_argument(
        "branch",
        help="Branch to switch to"
    )
    checkout_parser.add_argument(
        "-b",
        "--create-branch",
        action="store_true",
        help="Create and Switch to a new branch",
    )
    

     #branch command
    branch_parser =subparsers.add_parser("branch", help="List or manage branches")
    branch_parser.add_argument(
         "name",
        nargs="?",  # one or no value
        help="Name a new branch"
    ) 
    branch_parser.add_argument(
        "-b", "--create-branch",
        action="store_true",
        help="Create a new branch"
    ) 
    branch_parser.add_argument(
        "-d", "--delete-branch",
        action="store_true",
        help="Delete a new branch"
    ) 
    log_parser= subparsers.add_parser(
        "log",
        help="Show all the commits"
    )
    log_parser.add_argument(
        "-n", 
        "--max-count",
        type=int,
        default=10,
        help="Limit commits shown"
    ) 
   
    status_parser = subparsers.add_parser(
        "status",
        help="Show the git status"
    )

    return parser 

   
   
def handle_commands(args):
    """Handle commands after parsing."""
    repo = Repository()
    checkout=Checkout(repo)
    try:
        if args.command == "init":
            
            if not repo.init():
                print("Repository is already existing.")
        elif args.command == "add":
            if not repo.get_dir.exists():
                print("Not a git repository. Please initialize first.")
                return 
            for path in args.paths:
                repo.add(path)   
        elif args.command == "commit":
            if not repo.get_dir.exists(): 
                print("Not a git repository. Please initialize first.")
                return   
            author=args.author or "PyGit User at <email@example.com"
            committer =args.committer or args.author
            repo.commit(args.message, committer,author) 
        elif args.command == "checkout":
            if not repo.get_dir.exists():
                print("Not a git repository. Please initialize first.")
                return
            checkout.checkout(args.branch, args.create_branch)    

        elif args.command == "branch":
            if not repo.get_dir.exists():
                print("Not a git repository. Please initialize first.")
                return
            branch=Branch(repo)
            if args.create_branch:
                  
                  print(f"Creating branch {args.name}")
                  branch.create(args.name)
            elif args.delete_branch:
                 print(f"Deleting branch {args.name}")
                 branch.delete(args.name)
            elif args.list_branch:
                print("Listing all branches \n")
                branch_mg= branch.list()
                for mg in branch_mg:
                    print(mg)
                   

            else:
               print("No action provided. Use -b, -d, or -v.")

        elif args.command =="log":
            if not repo.get_dir.exists():
                print("Not a git repository. Please initialize first.")
                return
            log=Log(repo)
            log.log(args.max_count) #defult 10
        elif args.command == "status":
            if not repo.get_dir.exists():
                print("Not a git repository. Please initialize first.")
                return
            status =Status(repo) 
            status.status()   
        elif args.command == "gc":
            repo.garbage_collect()
            #
           
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
#

def main():
    parser = create_parser()
    parser = add_subparsers(parser)
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    handle_commands(args)


if __name__ == "__main__":
    main()

