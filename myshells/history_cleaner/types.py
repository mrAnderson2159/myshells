from typing import TypedDict, ParamSpec, TypeVar, Callable, Concatenate, Generic
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")
Row = TypeVar("Row", bound=tuple[object, ...])


class SplittedHistory(TypedDict):
    filtered: list[str]
    waste: list[str]


class HeadedColumns(TypedDict, Generic[Row]):
    headers: list[str]
    rows: list[Row]


class FullTables(TypedDict):
    ignored_lines: HeadedColumns[tuple[int, str, bool]]
    usual_suspects: HeadedColumns[tuple[str, bool]]
