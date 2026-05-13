r"""
Check tables at
    psql -d valescripts -c '\d hcln.ignored_lines' -c '\d hcln.usual_suspects'
"""

from functools import wraps
from typing import Callable, Concatenate, cast

from .types import P, T, Row, HeadedColumns, FullTables
from .config import get_db, IGNORED_LINES, USUAL_SUSPECTS
from ..postgres import Database


PASSWORD = "3b87553c56"  # TODO: Set to None or delete after testing!!!!!

DB = get_db(PASSWORD)


def with_db(func: Callable[Concatenate[Database, P], T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        with DB as db:
            return func(db, *args, **kwargs)

    return wrapper


def with_headers(
    headers: list[str],
) -> Callable[[Callable[P, list[Row]]], Callable[P, HeadedColumns[Row]]]:
    def decorator(func: Callable[P, list[Row]]) -> Callable[P, HeadedColumns[Row]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> HeadedColumns[Row]:
            return {
                "headers": headers,
                "rows": func(*args, **kwargs),
            }

        return wrapper

    return decorator


@with_headers(["line_number", "starts_with", "active"])
@with_db
def list_full_ignored_lines(db: Database) -> list[tuple[int, str, bool]]:
    return cast(
        list[tuple[int, str, bool]],
        db.read(
            f"""
        SELECT
            {IGNORED_LINES}.line_number,
            {USUAL_SUSPECTS}.starts_with,
            {IGNORED_LINES}.active
        FROM {IGNORED_LINES}
        LEFT JOIN {USUAL_SUSPECTS}
            ON {IGNORED_LINES}.suspect_id = {USUAL_SUSPECTS}.id
        """
        ),
    )


@with_headers(["starts_with", "active"])
@with_db
def list_full_usual_suspects(db: Database) -> list[tuple[str, bool]]:
    return cast(
        list[tuple[str, bool]],
        db.read(
            f"""
        SELECT starts_with, active FROM {USUAL_SUSPECTS}
        """
        ),
    )


def list_full_all() -> FullTables:
    return {
        "ignored_lines": list_full_ignored_lines(),
        "usual_suspects": list_full_usual_suspects(),
    }


@with_db
def get_ignored_lines(db: Database) -> list[int]:
    return db.read_column(
        f"SELECT line_number FROM {IGNORED_LINES} WHERE active = TRUE"
    )


@with_db
def get_usual_suspects(db: Database) -> list[str]:
    return db.read_column(
        f"SELECT starts_with FROM {USUAL_SUSPECTS} WHERE active = TRUE"
    )


@with_db
def add_ignored_line(db: Database, line_number: int) -> int:
    return db.write(
        f"INSERT INTO {IGNORED_LINES} (line_number) VALUES (%s)", (line_number,)
    )


@with_db
def activate_ignored_line(db: Database, line_number: int) -> int:
    return db.write(
        f"UPDATE {IGNORED_LINES} SET active = TRUE WHERE line_number = %s",
        (line_number,),
    )


@with_db
def deactivate_ignored_line(db: Database, line_number: int) -> int:
    return db.write(
        f"UPDATE {IGNORED_LINES} SET active = FALSE WHERE line_number = %s",
        (line_number,),
    )


@with_db
def delete_ignored_line(db: Database, line_number: int) -> int:
    return db.write(
        f"DELETE FROM {IGNORED_LINES} WHERE line_number = %s", (line_number,)
    )


@with_db
def add_usual_suspect(db: Database, starts_with: str) -> int:
    return db.write(
        f"INSERT INTO {USUAL_SUSPECTS} (starts_with) VALUES (%s)", (starts_with,)
    )


@with_db
def activate_usual_suspect(db: Database, starts_with: str) -> int:
    return db.write(
        f"UPDATE {USUAL_SUSPECTS} SET active = TRUE WHERE starts_with = %s",
        (starts_with,),
    )


@with_db
def deactivate_usual_suspect(db: Database, starts_with: str) -> int:
    return db.write(
        f"UPDATE {USUAL_SUSPECTS} SET active = FALSE WHERE starts_with = %s",
        (starts_with,),
    )


@with_db
def delete_usual_suspect(db: Database, starts_with: str) -> int:
    return db.write(
        f"DELETE FROM {USUAL_SUSPECTS} WHERE starts_with = %s",
        (starts_with,),
    )


@with_db
def clear_ignored_lines(db: Database) -> int:
    return db.write(f"DELETE FROM {IGNORED_LINES}")


@with_db
def clear_usual_suspects(db: Database) -> int:
    return db.write(f"DELETE FROM {USUAL_SUSPECTS}")


def clear_all() -> int:
    il = clear_ignored_lines()
    us = clear_usual_suspects()
    return il + us
