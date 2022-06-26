"""
Test cases for Order Model

"""
import os
import logging
import unittest
import random
from service import app
from service.models import Order, Item, DataValidationError, db, OrderStatus
from tests.factories import OrderFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  Order   M O D E L   T E S T   C A S E S
######################################################################
class TestOrder(unittest.TestCase):
    """ Test Cases for Order Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################