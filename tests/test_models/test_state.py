#!/usr/bin/python3
"""Unit test for state model """
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """state class test """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """test for name"""
        new = self.value()
        self.assertEqual(type(new.name), str)
