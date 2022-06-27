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
        db.session.close()

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

    def test_create_an_order(self):
        """It should Create an Order and assert that it exists"""
        fake_order = OrderFactory()
        order = Order(
            customer_id=fake_order.customer_id,
            tracking_id=fake_order.tracking_id,
            status=fake_order.status,
        )
        self.assertIsNotNone(order)
        self.assertEqual(order.id, None)
        self.assertEqual(order.customer_id, fake_order.customer_id)
        self.assertEqual(order.tracking_id, fake_order.tracking_id)
        self.assertEqual(order.status, fake_order.status)

    def test_add_an_order(self):
        """It should Create an order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_read_order(self):
        """It should Read an order"""
        order = OrderFactory()
        order.create()

        # Read it back
        found_order = Order.find(order.id)
        self.assertEqual(found_order.id, order.id)
        self.assertEqual(found_order.customer_id, order.customer_id)
        self.assertEqual(found_order.tracking_id, order.tracking_id)
        self.assertEqual(found_order.created_time, order.created_time)
        self.assertEqual(found_order.status, order.status)
        self.assertEqual(found_order.order_items, [])

    def test_list_all_orders(self):
        """It should List all Orders in the database"""
        orders = Order.all()
        # self.assertEqual(orders, [])
        for order in OrderFactory.create_batch(3):
            order.create()
        # Assert that there are not 3 orders in the database
        orders = Order.all()
        self.assertEqual(len(orders), 3)

    def test_find_list_by_customer_id(self):
        """It should Find an Order by customer_id"""
        order = OrderFactory()
        order.create()
        # Fetch it from database by customer_id
        same_order = Order.find_by_customer(order.customer_id)[0]
        self.assertEqual(same_order.id, order.id)
        self.assertEqual(same_order.customer_id, order.customer_id)

    def test_serialize_an_order(self):
        """It should Serialize an order"""
        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()

        serial_order = order.serialize()
        self.assertEqual(serial_order["id"], order.id)
        self.assertEqual(serial_order["customer_id"], order.customer_id)
        self.assertEqual(serial_order["tracking_id"], order.tracking_id)
        self.assertEqual(serial_order["status"], order.status.name)
        self.assertEqual(len(serial_order["order_items"]), 1)
        items = serial_order["order_items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["order_id"], item.order_id)
        self.assertEqual(items[0]["product_id"], item.product_id)
        self.assertEqual(items[0]["quantity"], item.quantity)
        self.assertEqual(items[0]["price"], item.price)

    def test_deserialize_an_order(self):
        """It should Deserialize an order"""
        order = OrderFactory()
        order.order_items.append(ItemFactory())
        order.create()
        serial_order = order.serialize()
        new_order = Order()
        new_order.deserialize(serial_order)
        self.assertEqual(new_order.customer_id, order.customer_id)
        self.assertEqual(new_order.tracking_id, order.tracking_id)
        self.assertEqual(new_order.status, order.status)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an order with a KeyError"""
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an order with a TypeError"""
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])
    
    def test_add_order_item(self):
        """It should Create an item with an order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1) 

        new_order = Order.find(order.id)
        self.assertEqual(new_order.order_items[0].id, item.id)

        item2 = ItemFactory()
        order.order_items.append(item2)
        order.update()

        new_order = Order.find(order.id)
        self.assertEqual(len(new_order.order_items), 2)
        self.assertEqual(new_order.order_items[1].id, item2.id)

    def test_read_order_item(self):
        """It should Read an item"""
        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()

        # Read it back
        found_item = Item.find(item.id)
        self.assertEqual(found_item.id, item.id)
        self.assertEqual(found_item.order_id, order.id)
        self.assertEqual(found_item.product_id, item.product_id)
        self.assertEqual(found_item.quantity, item.quantity)
        self.assertEqual(found_item.price, item.price)