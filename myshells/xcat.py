import argparse
import os
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Concatenate and print files under a directory, with explicit ignores"
    )
    parser.add_argument("path", help="Root directory to scan")
    parser.add_argument(
        "-I",
        "--ignore",
        action="append",
        default=[],
        help="Path to ignore (file or directory). Can be repeated.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    root = Path(args.path).resolve()

    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        sys.exit(1)

    output_chunks = []

    # Check if root is a file instead of a directory
    if root.is_file():
        try:
            with open(root, "r", encoding="utf-8", errors="ignore") as f:
                output_chunks.append(f"\n\n----------> {root} <----------\n\n")
                output_chunks.append(f.read())
        except Exception as e:
            print(f"error: could not read file: {root} ({e})", file=sys.stderr)
            sys.exit(1)
    else:
        # Resolve ignore paths
        ignore_absolutes = set()
        ignore_everywhere = set()
        for ig in args.ignore:
            if ig.startswith("/"):
                ignore_absolutes.add(Path(ig).resolve())
            else:
                ignore_everywhere.add(ig)

        for current_root, dirs, files in os.walk(root):
            current_root = Path(current_root).resolve()

            # Prune ignored directories
            pruned_dirs = []
            for d in dirs:
                dir_path = (current_root / d).resolve()
                if dir_path in ignore_absolutes or d in ignore_everywhere:
                    if dir_path in ignore_absolutes:
                        ignore_absolutes.remove(dir_path)

                    pruned_dirs.append(d)

            dirs[:] = [d for d in dirs if d not in pruned_dirs]

            for file in files:
                file_path = (current_root / file).resolve()

                if file_path in ignore_absolutes or file in ignore_everywhere:
                    if file_path in ignore_absolutes:
                        ignore_absolutes.remove(file_path)
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        output_chunks.append(
                            f"\n\n----------> {file_path} <----------\n\n"
                        )
                        output_chunks.append(f.read())
                except Exception as e:
                    print(
                        f"warning: could not read file: {file_path} ({e})",
                        file=sys.stderr,
                    )

    print("".join(output_chunks))


if __name__ == "__main__":
    main()
