"""
Test cases for Order Model

"""
import os
import logging
import unittest
from service.models import Order, Item, DataValidationError, db
from tests.factories import OrderFactory, ItemFactory

######################################################################
#  Order   M O D E L   T E S T   C A S E S
######################################################################
class TestOrder(unittest.TestCase):
    """ Test Cases for Order Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    
