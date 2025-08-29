import argparse
from pathlib import Path


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

class Repository:
     def __init__(self, path="."):
          self.path =Path(path).resolve()
          self.get_dir = self.path / ".pygit"

          self.objects_dir = self.get_dir / "objects"
          self.refs_dir = self.get_dir / "refs"
          self.head_file = self.get_dir / "HEAD"

          self.index_file = self.get_dir/"index"

     def init(self)->bool:
          # create the file with the current initialization
          self.get_dir.mkdir() 
          self.objects_dir.mkdir()
          self.refs_dir.mkdir()     

def main():
    parser = argparse.ArgumentParser(
        description="Python - A simple git CLI"
    )
    subparsers=parser.add_subparsers(
    dest="command",
    help="Available Commands"
    )

    #init command
    init_parser = subparsers.add_parser(
        "init",
        help="Intialize a new Git Repository"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "init":
             pass

    except Exception as e:
          print(f"Error:{e}")
main()