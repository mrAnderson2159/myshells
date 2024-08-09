"""
Defines the :class:`Database` class which allows to interface with a JSON
file (usually database.json) storing project's datas.
"""

import json
import os
import sys
from typing import *

from src.v_tree_dict import VTreeDict

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from colors import *


class Database:
    def __init__(self, dbpath: str) -> None:
        """Provides the tools to interface with a JSON file storing project's data.
        Creates a dictionary version of the database in its db attribute.
        Every db[key] is an instance of :py:class:`VTreeDict` class.

        :param dbpath: the path to the database file (usually database.json)
        :type dbpath: string
        """
        self.dbpath = dbpath
        self.db: Dict[str:VTreeDict] = {}
        self.load()

    def __getitem__(self, key: str) -> VTreeDict:
        """Returns the value of key at the first level of db dictionary.

        :param key: the searched key
        :type key: str
        :return: the db[key] value
        :rtype: VTreeDict
        """
        return self.db[key]

    def __setitem__(self, key: str, value: VTreeDict) -> dict:
        """Changes the value of a key to a given value

        :param key: the searched key
        :type key: str
        :param value: a VTree_dict data object
        :type value: VTreeDict
        :return: the database itself
        :rtype: dict
        """
        self.db[key] = value
        return self.db

    def __delitem__(self, key: str) -> VTreeDict:
        """Remove a db key

        :param key: the searched key
        :type key: str
        :return: the removed key
        :rtype: VTreeDict
        """
        db = self.db[key]
        del self.db[key]
        return db

    def __repr__(self):
        """Return the db dictionary`

        :return: db dictionary
        :rtype: dict
        """
        return self.db

    def __str__(self):
        """Return the string version of db dictionary

        :return: string db dictionary
        :rtype: str
        """
        return str(self.db)

    def add(self, vt_dict: VTreeDict) -> None:
        """Add a :class:`VTree_dict` dictionary in the database
        at obj.name key

        :param vt_dict: the VTree_dict to add
        :type vt_dict: VTreeDict
        """
        self[vt_dict.name] = vt_dict

    def load(self) -> None:
        """Tries to load the JSON database, turn each of its keys to a :class:`VTreeDict`
        using the :meth:`VTreeDict.dictize` method
        """
        try:
            with open(self.dbpath, 'r') as db:
                self.db = json.loads(db.read())
            for database, value in self.db.items():
                self.db[database] = VTreeDict.dictize(value)
        except json.JSONDecodeError:
            yellow("[WARNING]: database not loaded")

    def write(self) -> None:
        """Writes the db dictionary into the JSON database
        """
        with open(self.dbpath, 'w') as db:
            db.write(json.dumps({key: value.dict() for key, value in self.db.items()}))

    def update(self, db: dict) -> None:
        """ Substitute the database with the db dictionary then write it to the JSON database

        :param db: the new database
        :type db: dict
        """
        self.db = db
        self.write()

    def destroy(self) -> dict:
        """Reset the database and return it

        :return: the database before being erased
        :rtype: dict
        """
        db = self.db
        self.db = {}
        return db

    def destroy_and_write(self) -> dict:
        """Reset the database both in this class and in the JSON database, then return it

        :return: the database before being erased
        :rtype: dict
        """
        db = self.destroy()
        self.write()
        return db
