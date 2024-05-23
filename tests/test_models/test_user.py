#!/usr/bin/python3
"""Unit test for user model"""
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """user class test"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """test for first name"""
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """test for last name"""
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """test for email"""
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """test password"""
        new = self.value()
        self.assertEqual(type(new.password), str)
