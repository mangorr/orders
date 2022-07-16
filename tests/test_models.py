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
        """It should Create an Order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_order(self):
        """It should Update an Order"""
        order = OrderFactory()
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)

        # Fetch it back
        order = Order.find(order.id)
        order.tracking_id = 8888
        order.status = OrderStatus.CANCELLED
        order.update()

        # Fetch it back again
        order = Order.find(order.id)
        self.assertEqual(order.tracking_id, 8888)
        self.assertEqual(order.status.name, OrderStatus.CANCELLED.name)

    def test_read_order(self):
        """It should Read an Order"""
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

    def test_delete_an_order(self):
        """It should Delete an Order from the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        order = orders[0]
        order.delete()
        orders = Order.all()
        self.assertEqual(len(orders), 0)

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
    
    def test_find_by_status(self):
        """It should Find Pets by Gender"""
        orders = OrderFactory.create_batch(10)
        for order in orders:
            order.create()
        order_status = orders[0].status
        count = len([order for order in orders if order.status == order_status])
        found = Order.find_by_status(order_status)
        self.assertEqual(found.count(), count)
        for order in found:
            self.assertEqual(order.status, order_status)

    def test_serialize_an_order(self):
        """It should Serialize an Order"""
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
        """It should Deserialize an Order"""
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
        """It should not Deserialize an Order with a KeyError"""
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an Order with a TypeError"""
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an Item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an Item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])
    
    def test_add_order_item(self):
        """It should Create an Item with an order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        item = ItemFactory()
        order.order_items.append(item)
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

    def test_update_order_item(self):
        """It should Update an order Item"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        item = ItemFactory()
        order.order_items.append(item)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Fetch it back
        order = Order.find(order.id)
        old_item = order.order_items[0]
        print("%r", old_item)
        self.assertEqual(old_item.product_id, item.product_id)
        self.assertEqual(old_item.quantity, item.quantity)
        self.assertEqual(old_item.price, item.price)
        # Change the product_id, quantity, price
        old_item.product_id = 9999
        old_item.quantity = 8888
        old_item.price = 7777
        order.update()

        # Fetch it back again
        order = Order.find(order.id)
        item = order.order_items[0]
        self.assertEqual(item.product_id, 9999)
        self.assertEqual(item.quantity, 8888)
        self.assertEqual(item.price, 7777)

    def test_read_order_item(self):
        """It should Read an Item"""
        order = OrderFactory()
        item = ItemFactory()
        order.order_items.append(item)
        order.create()

        # Read it back
        found_item = Item.find(item.id)
        self.assertEqual(found_item.id, item.id)
        self.assertEqual(found_item.order_id, order.id)
        self.assertEqual(found_item.product_id, item.product_id)
        self.assertEqual(found_item.quantity, item.quantity)
        self.assertEqual(found_item.price, item.price)

    def test_delete_order_item(self):
        """It should Delete an order Item"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Fetch it back
        order = Order.find(order.id)
        item = order.order_items[0]
        item.delete()
        order.update()

        # Fetch it back again
        order = Order.find(order.id)
        self.assertEqual(len(order.order_items), 0)