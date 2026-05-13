from ..postgres import Database

IGNORED_LINES = "ignored_lines"
USUAL_SUSPECTS = "usual_suspects"
DB_SCHEMA = "hcln"
USER = "vale_test"
DBNAME = "valescripts_test"


def get_db(password: str | None = None) -> Database:
    return Database(schema=DB_SCHEMA, password=password, user=USER, dbname=DBNAME)
