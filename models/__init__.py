#!/usr/bin/python3
"""This module create and instantiates unique FileStorage instance for the
application.
A unique FileStorage/DBStorage instance for all models
"""
import os

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage = DBStorage() if os.getenv(
    'HBNB_TYPE_STORAGE') == 'db' else FileStorage()

storage.reload()
