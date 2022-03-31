"""
"""
import os
import logging
import unittest

from api.app import create_app

class ApiTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["TEST_MODE"] = "True"
        api_app = create_app()
