import os
import re
import tempfile
from datetime import datetime

from .store import get_ignored_lines, get_usual_suspects
from .types import SplittedHistory


def get_line_start(line: str) -> str | None:
    # treat empty / whitespace lines as separators
    if line.strip() == "":
        return ""  # forced separator

    # example: ": 1760254723:0;ls -la"
    match = re.match(r"^:\s\d{10}:0;(.*)$", line)
    if match:
        return match.group(1)

    return None


def _get_history_path() -> str:
    history_path = os.environ.get("HISTFILE")

    if not history_path:
        raise RuntimeError(
            "HISTFILE environment variable is not set. "
            "You can set it with 'export HISTFILE=/path/to/history'."
        )

    if not os.path.isfile(history_path):
        raise RuntimeError(
            f"HISTFILE path '{history_path}' does not exist or is not a file."
        )

    return history_path


def _get_backup_dir() -> str:
    backup_dir = os.path.expanduser("~/histfile_bak")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def _create_history_backup(history_path: str) -> None:
    backup_dir = _get_backup_dir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = os.path.join(backup_dir, f"history_{timestamp}.bak")

    with open(history_path, "r", encoding="utf-8", errors="ignore") as src, open(
        backup_path, "w", encoding="utf-8", errors="ignore"
    ) as dst:
        dst.write(src.read())


def _cleanup_history_backups(max_backups: int = 5) -> None:
    if max_backups < 1:
        raise ValueError("max_backups must be at least 1.")

    backup_dir = _get_backup_dir()

    files = [
        os.path.join(backup_dir, f)
        for f in os.listdir(backup_dir)
        if f.endswith(".bak")
    ]

    if len(files) <= max_backups:
        return

    # ordina per data di modifica (più vecchi prima)
    files.sort(key=lambda f: os.path.getmtime(f))

    to_delete = files[:-max_backups]

    for f in to_delete:
        os.remove(f)


def get_history(history_path: str | None = None) -> list[str]:
    history_path = history_path or _get_history_path()

    with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()


def split_history(
    history: list[str],
    suspects: set[str],
    *,
    use_ignored_lines: bool = True,
    use_usual_suspects: bool = True,
) -> SplittedHistory:
    ignored_lines = set(get_ignored_lines()) if use_ignored_lines else set()
    usual_suspects = set(get_usual_suspects()) if use_usual_suspects else set()
    suspects = suspects | usual_suspects

    filtered: list[str] = []
    waste: list[str] = []

    current_entry: list[str] = []
    current_command_start: str | None = None
    entry_number = 0

    def flush_current_entry() -> None:
        nonlocal current_entry, current_command_start, entry_number

        if not current_entry:
            return

        entry_number += 1
        entry_text = "".join(current_entry)

        if entry_number in ignored_lines:
            filtered.append(entry_text)
        elif current_command_start is not None and any(
            current_command_start.startswith(suspect) for suspect in suspects
        ):
            waste.append(entry_text)
        else:
            filtered.append(entry_text)

        current_entry = []
        current_command_start = None

    for line in history:
        parsed_line = get_line_start(line)

        if parsed_line is not None:
            flush_current_entry()
            current_entry = [line]
            current_command_start = parsed_line
        else:
            current_entry.append(line)

    flush_current_entry()

    return {"filtered": filtered, "waste": waste}


def write_history(
    entries: list[str],
    *,
    history_path: str | None = None,
    make_backup: bool = True,
    max_backups: int = 5,
) -> None:
    history_path = history_path or _get_history_path()
    history_dir = os.path.dirname(history_path) or "."

    if make_backup:
        _create_history_backup(history_path)
        _cleanup_history_backups(max_backups)

    tmp_path: str | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=history_dir,
            delete=False,
            encoding="utf-8",
            errors="ignore",
        ) as tmp:
            tmp.write("".join(entries))
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_path = tmp.name

        os.replace(tmp_path, history_path)
    except Exception:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def rewrite_history(
    suspects: set[str],
    *,
    use_ignored_lines: bool = True,
    use_usual_suspects: bool = True,
    make_backup: bool = True,
    max_backups: int = 5,
) -> SplittedHistory:
    history_path = _get_history_path()
    history = get_history(history_path)

    splitted = split_history(
        history,
        suspects,
        use_ignored_lines=use_ignored_lines,
        use_usual_suspects=use_usual_suspects,
    )

    write_history(
        splitted["filtered"],
        history_path=history_path,
        make_backup=make_backup,
        max_backups=max_backups,
    )
    return splitted


def _count_lines(entries: list[str]) -> int:
    return sum(len(entry.splitlines()) for entry in entries)


def _test() -> None:
    suspects = {"hide", "virtual", "gocryptfs -", "cd backend"}

    history = get_history()
    splitted = split_history(history, suspects)

    len_history = len(history)
    len_filtered_entries = len(splitted["filtered"])
    len_waste_entries = len(splitted["waste"])

    len_filtered_lines = _count_lines(splitted["filtered"])
    len_waste_lines = _count_lines(splitted["waste"])

    print(f"Original file lines: {len_history}")
    print(f"Filtered entries: {len_filtered_entries}")
    print(f"Waste entries: {len_waste_entries}")
    print(f"Filtered file lines: {len_filtered_lines}")
    print(f"Waste file lines: {len_waste_lines}")
    print(f"Sum of classified file lines: {len_filtered_lines + len_waste_lines}")
    print(
        f"Difference between original and classified lines: "
        f"{len_history - (len_filtered_lines + len_waste_lines)}"
    )

    for entry in splitted["waste"]:
        print(entry)


if __name__ == "__main__":
    _test()
