#!/usr/bin/python3
"""This module defines the Unittest test cases for the HBNBCommand console
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """Defines the test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Checks the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cmndr = HBNBCommand()
            cmndr.onecmd('create City name="Texas"')
            mdl_id = f.getvalue().strip()
            clear_stream(f)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cmndr.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", f.getvalue().strip())
            clear_stream(f)
            cmndr.onecmd('create User name="Mahari" age=31 height=5.9')
            mdl_id = f.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(f)
            cmndr.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'Mahari'", f.getvalue().strip())
            self.assertIn("'age': 31", f.getvalue().strip())
            self.assertIn("'height': 5.9", f.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Checks the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cmndr = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cmndr.onecmd('create User')
            # creating a User instance
            clear_stream(f)
            cmndr.onecmd('create User email="mhr9@yahoo.com" password="123"')
            mdl_id = f.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('mhr9@yahoo.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Checks the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cmndr = HBNBCommand()
            # showing a User instance
            obj = User(email="mhr9@yahoo.com", password="123")
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cmndr.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                f.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(f)
            cmndr.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('mhr9@yahoo.com', result)
            self.assertIn('123', result)
            self.assertIn('mhr9@yahoo.com', f.getvalue())
            self.assertIn('123', f.getvalue())
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Checks the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cmndr = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            cmndr.onecmd('create State name="Tigray"')
            clear_stream(f)
            cmndr.onecmd('count State')
            cnt = f.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(f)
            cmndr.onecmd('count State')
            cursor.close()
            dbc.close()
