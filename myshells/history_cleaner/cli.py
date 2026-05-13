from argparse import ArgumentParser, Namespace
from . import store as sv
from typing import Any, Mapping
from rich.table import Table
from rich.console import Console
from rich import box
from .types import HeadedColumns

console = Console()


def cap(string: str, *, all: bool = False) -> str:
    words = string.strip().split("_")

    if all:
        words = [word.capitalize() for word in words]
    else:
        words[0] = words[0].capitalize()

    return " ".join(words)


def print_table(data: HeadedColumns[tuple[Any, ...]]) -> None:
    table = Table(box=box.SIMPLE_HEAVY)

    for header in data["headers"]:
        table.add_column(cap(header), style="cyan", no_wrap=True)

    for row in data["rows"]:
        table.add_row(*(str(cell) for cell in row))

    console.print(table)


def print_full_tables(data: Mapping[str, HeadedColumns[tuple[Any, ...]]]) -> None:
    for name, table_data in data.items():
        console.print(f"\n[bold yellow]{cap(name, all=True)}[/bold yellow]")
        print_table(table_data)


def build_parser() -> ArgumentParser:

    parser = ArgumentParser(
        prog="hcln",
        description="History Cleaner CLI. A tool to clean your shell history by filtering out "
        "unwanted commands.",
    )

    subparsers = parser.add_subparsers(dest="action", required=True)

    # actions that don't accept "all" as a kind of entry
    for action, help_text in (
        ("add", "Allows you to add a new entry to the database."),
        ("activate", "Activates an existing entry in the database."),
        ("deactivate", "Deactivates an existing entry in the database."),
        ("delete", "Deletes an existing entry from the database."),
    ):
        action_parser = subparsers.add_parser(action, help=help_text)

        action_parser.add_argument(
            "kind",
            choices=["ignored-line", "usual-suspect", "il", "us"],
            help="'il' = ignored line, 'us' = usual suspect.",
        )
        action_parser.add_argument(
            "value",
            help="The value of the entry. For 'ignored-line' it should be a line number, "
            "for 'usual-suspect' it should be the starting string of a command.",
        )

    # actions that accept "all" as a kind of entry
    for action, help_text in (
        ("list", "Lists entries in the database."),
        ("cleardb", "Clears entries in the database."),
    ):
        action_parser = subparsers.add_parser(action, help=help_text)

        action_parser.add_argument(
            "kind",
            choices=["ignored-line", "usual-suspect", "il", "us", "all"],
            help="'il' = ignored line, 'us' = usual suspect, 'all' = all entries of any kind.",
        )

    action_parser = subparsers.add_parser(
        "clean",
        help="Removes provided commands from user's HISTFILE.",
    )

    action_parser.add_argument(
        "commands",
        nargs="*",
        help="Specific command prefixes to remove from history.",
    )

    action_parser.add_argument(
        "-I",
        "--no-ignored-lines",
        action="store_true",
        help="Do not use ignored lines from the database.",
    )

    action_parser.add_argument(
        "-U",
        "--no-usual-suspects",
        action="store_true",
        help="Do not use usual suspects from the database.",
    )

    return parser


def handle_args(args: Namespace):
    if args.action == "clean":
        return

    match (args.action, args.kind):
        case ("add", "ignored-line" | "il"):
            sv.add_ignored_line(int(args.value))
        case ("add", "usual-suspect" | "us"):
            sv.add_usual_suspect(args.value)
        case ("activate", "ignored-line" | "il"):
            sv.activate_ignored_line(int(args.value))
        case ("activate", "usual-suspect" | "us"):
            sv.activate_usual_suspect(args.value)
        case ("deactivate", "ignored-line" | "il"):
            sv.deactivate_ignored_line(int(args.value))
        case ("deactivate", "usual-suspect" | "us"):
            sv.deactivate_usual_suspect(args.value)
        case ("delete", "ignored-line" | "il"):
            sv.delete_ignored_line(int(args.value))
        case ("delete", "usual-suspect" | "us"):
            sv.delete_usual_suspect(args.value)
        case ("list", "ignored-line" | "il"):
            res = sv.list_full_ignored_lines()
            print_table(res)
        case ("list", "usual-suspect" | "us"):
            res = sv.list_full_usual_suspects()
            print_table(res)
        case ("list", "all"):
            res = sv.list_full_all()
            print_full_tables(res)  # type: ignore
        case ("cleardb", "ignored-line" | "il"):
            sv.clear_ignored_lines()
        case ("cleardb", "usual-suspect" | "us"):
            sv.clear_usual_suspects()
        case ("cleardb", "all"):
            sv.clear_all()
        case _:
            print("Invalid command. Use --help for more information.")


def main():
    parser = build_parser()
    args = parser.parse_args()
    handle_args(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
