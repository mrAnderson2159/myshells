import psycopg
from getpass import getpass

from typing import TypedDict, TypeVar, cast
from psycopg.abc import QueryNoTemplate, Params

Config = TypedDict(
    "Config",
    {
        "host": str,
        "port": int,
        "user": str,
        "password": str,
        "dbname": str,
    },
)

T = TypeVar("T")


class Database:
    def __init__(
        self,
        *,
        schema: str,
        host: str = "localhost",
        port: int = 5432,
        user: str = "vale",
        password: str | None = None,
        dbname: str = "valescripts",
    ) -> None:
        if not schema or not isinstance(schema, str) or not schema.isidentifier():
            raise ValueError(
                "Schema name must be a non-empty string and a valid identifier."
            )

        if password is None:
            password = getpass(f"Password for user {user}: ")

        self.__config: Config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "dbname": dbname,
        }
        self.schema = schema
        self.__connection: psycopg.Connection | None = None

    def __enter__(self) -> "Database":
        self.__connection = psycopg.connect(
            host=self.__config["host"],
            port=self.__config["port"],
            user=self.__config["user"],
            password=self.__config["password"],
            dbname=self.__config["dbname"],
            options=f"-c search_path={self.schema}",
        )
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.__connection is not None:
            if exc:
                self.__connection.rollback()
            else:
                self.__connection.commit()
            self.__connection.close()

    def read(
        self,
        query: QueryNoTemplate,
        params: Params | None = None,
    ) -> list[tuple[object, ...]]:
        if self.__connection is None:
            raise RuntimeError("Database connection is not established.")

        with self.__connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def read_column(
        self,
        query: QueryNoTemplate,
        params: Params | None = None,
    ) -> list[T]:
        rows = self.read(query, params)
        return [cast(T, row[0]) for row in rows]

    def write(self, query: QueryNoTemplate, params: Params | None = None) -> int:
        if self.__connection is None:
            raise RuntimeError("Database connection is not established.")

        with self.__connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
