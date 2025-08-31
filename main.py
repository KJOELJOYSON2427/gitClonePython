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

import argparse
import sys



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

    return parser 

def handle_commands(args):
    """Handle commands after parsing."""
    repo = Repository()
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
            repo.commit(args.message, author)        
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

main()