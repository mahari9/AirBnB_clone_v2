#!/usr/bin/python3
"""Defines unittests for models/city.py."""
import os

from models.city import City
from tests.test_models.test_base_model import TestBasemodel


class TestCity(TestBasemodel):
    """Indicates the tests for the City model
       Inherits from the base test class (TestBasemodel).
    """
    def __init__(self, *args, **kwargs):
        """Initializes the test instance."""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Tests the type of state_id attribute of a City instance."""
        new = self.value()
        self.assertEqual(
            type(new.state_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_name(self):
        """Test the name attribute of a new City instance."""
        new = self.value()
        self.assertEqual(
            type(new.name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )
