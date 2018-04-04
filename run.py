
from languages import language_factory
import argparse
import sys

def create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="proj_path", help="the project path")
    parser.add_argument("-L", dest="local_libs", help="the local libs to include")
    parser.add_argument("-R", dest="remote_libs", help="the remote libs to include")
    parser.add_argument("-l", dest="lang", help="the language of the project")
    return parser

if __name__ == "__main__":
    parser = create_args()
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit()
    args = parser.parse_args()
    if not args.proj_path or not args.lang:
        print("Need value for -p: project_path and -l: language ")
        sys.exit()
    options = {"project_path": args.proj_path}
    if args.lang.lower() in {"c", "c++"}:
        if args.local_libs is not None:
            options["local_libs"] = args.local_libs.split(",")
        if args.remote_libs is not None:
            options["remote_libs"] = args.remote_libs.split(",")
    lang_temp = language_factory(args.lang.lower(), options)
    if not lang_temp:
        print("Unknown or Unsupported Language")
        sys.exit()
    lang_temp.create_template()