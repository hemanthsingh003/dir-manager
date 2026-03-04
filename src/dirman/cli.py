import argparse
import sys
from pathlib import Path

from .core import DirManager


def main():
    parser = argparse.ArgumentParser(prog="dirman", description="Git-like directory manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize/add a directory")
    init_parser.add_argument("name", help="Name for the directory")
    init_parser.add_argument("path", help="Path to the directory")

    add_parser = subparsers.add_parser("add", help="Add a directory (alias for init)")
    add_parser.add_argument("name", help="Name for the directory")
    add_parser.add_argument("path", help="Path to the directory")

    remove_parser = subparsers.add_parser("remove", help="Remove a directory from tracking")
    remove_parser.add_argument("name", help="Name of the directory to remove")

    subparsers.add_parser("list", help="List all tracked directories")

    status_parser = subparsers.add_parser("status", help="Show status of tracked directories")

    get_parser = subparsers.add_parser("get", help="Get details of a tracked directory")
    get_parser.add_argument("name", help="Name of the directory")

    args = parser.parse_args()

    dm = DirManager()

    if args.command in ("init", "add"):
        result = dm.init(args.name, args.path)
        print(result)
    elif args.command == "remove":
        result = dm.remove(args.name)
        print(result)
    elif args.command == "list":
        dirs = dm.list()
        if not dirs:
            print("No directories tracked")
        for name, path in dirs:
            print(f"{name}: {path}")
    elif args.command == "status":
        statuses = dm.status()
        if not statuses:
            print("No directories tracked")
        for s in statuses:
            status = "✓" if s["exists"] else "✗"
            print(f"{status} {s['name']}: {s['path']}")
    elif args.command == "get":
        info = dm.get(args.name)
        if info:
            print(f"Name: {args.name}")
            print(f"Path: {info['path']}")
        else:
            print(f"Directory '{args.name}' not found")
            sys.exit(1)


if __name__ == "__main__":
    main()
