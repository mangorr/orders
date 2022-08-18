"""
Order API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestOrderService
"""

import os
import logging
from unittest import TestCase
from service import app
from service.models import db, Order, init_db, OrderStatus
from tests.factories import OrderFactory, ItemFactory
from service.utils import status  # HTTP Status Codes

BASE_URL = "/api/orders"
ALL_ITEM_URL = "/api/items"

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class Test(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.app = app.test_client()
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_orders(self, count):
        """Factory method to create orders in bulk"""
        orders = []
        for _ in range(count):
            order = OrderFactory()
            resp = self.app.post(BASE_URL, json=order.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Order",
            )
            new_order = resp.get_json()
            order.id = new_order["id"]
            orders.append(order)
        return orders

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(b'Order REST API Service', resp.data)

    def test_health(self):
        """It should be healthy"""
        resp = self.app.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['message'], 'OK')

    def test_create_order(self):
        """It should Create a new Order"""
        order = OrderFactory()
        resp = self.app.post(
            BASE_URL, json=order.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_order = resp.get_json()
        self.assertEqual(new_order["customer_id"], order.customer_id, "Customer id does not match")
        self.assertEqual(new_order["tracking_id"], order.tracking_id, "Tracking id does not match")
        self.assertEqual(new_order["status"], order.status.name, "Status does not match")
        self.assertEqual(len(new_order["order_items"]), len(order.order_items), "Items does not match")

        # Check that the location header was correct by getting it
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_order = resp.get_json()
        self.assertEqual(new_order["customer_id"], order.customer_id, "Customer id does not match")
        self.assertEqual(new_order["tracking_id"], order.tracking_id, "Tracking id does not match")
        self.assertEqual(new_order["status"], order.status.name, "Status does not match")
        self.assertEqual(new_order["order_items"], order.order_items, "Items does not match")

    def test_update_order(self):
        """It should Update an existing Order"""
        # create an Order to update
        test_order = OrderFactory()
        resp = self.app.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = resp.get_json()
        new_order_id = new_order["id"]
        new_order["customer_id"] = 9999
        new_order["tracking_id"] = 8888
        new_order["status"] = OrderStatus.CANCELLED.name

        resp = self.app.put(f"{BASE_URL}/{new_order_id}", json=new_order)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_order = resp.get_json()
        self.assertEqual(updated_order["customer_id"], 9999)
        self.assertEqual(updated_order["tracking_id"], 8888)
        self.assertEqual(updated_order["status"], OrderStatus.CANCELLED.name)

    def test_update_order_not_found(self):
        """It should not Update an Order that is not found"""
        # order = OrderFactory()
        # print(type(order.id))
        # print(type(order.customer_id))
        # print(type(order.tracking_id))
        # print(type(order.status))
        # print(type(order.status))
        order = {}
        order["id"] = 1234
        order["customer_id"] = 9999
        order["tracking_id"] = 8888
        order["status"] = OrderStatus.CANCELLED.name
        # order have not created yet
        resp = self.app.put(
            f"{BASE_URL}/1234",
            json=order,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        """It should Delete an Order"""
        # get the id of an order
        order = self._create_orders(1)[0]
        resp = self.app.delete(f"{BASE_URL}/{order.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_orders_wrong_content_type(self):
        """ It should not Create an Order with wrong content type """
        order = OrderFactory()
        resp = self.app.post(BASE_URL,
                             json=order.serialize(),
                             content_type='application/xml')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_no_data(self):
        """It should not Create an Order with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_order(self):
        """It should Read a single Order"""
        # get the id of an order
        order = self._create_orders(1)[0]
        resp = self.app.get(
            f"{BASE_URL}/{order.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], order.id)

    def test_get_order_not_found(self):
        """It should not Read an Order that is not found"""
        resp = self.app.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_with_method_not_supported(self):
        """It should not Read an Order with wrong method"""
        # test for error_handlers
        resp = self.app.post(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_order_list(self):
        """ It should List Orders """
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

        # create three orders and name sure it appears in the list
        self._create_orders(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_cancel_order_succeed(self):
        """It should Cancel an existing Order"""
        # create an Order to cancel
        test_order = OrderFactory()
        resp = self.app.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # generate the request
        new_order = resp.get_json()
        new_order_id = new_order["id"]
        new_order["customer_id"] = 9999
        new_order["tracking_id"] = 8888
        new_order["status"] = OrderStatus.PAID.name
        resp = self.app.put(f"{BASE_URL}/{new_order_id}", json=new_order)
        print("3333")
        resp = self.app.put(f"{BASE_URL}/{new_order_id}/cancel", json=new_order)
        print("2222")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        print("1111")
        updated_order = resp.get_json()
        self.assertEqual(updated_order["customer_id"], 9999)
        self.assertEqual(updated_order["tracking_id"], 8888)
        self.assertEqual(updated_order["status"], OrderStatus.CANCELLED.name)

    def test_cancel_order_failed(self):
        """It should not Cancel an existing Order"""
        # create an Order to cancel
        test_order = OrderFactory()
        resp = self.app.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # generate the request
        new_order = resp.get_json()
        new_order_id = new_order["id"]
        new_order["customer_id"] = 1111
        new_order["tracking_id"] = 2222
        new_order["status"] = OrderStatus.DELIVERED.name
        resp = self.app.put(f"{BASE_URL}/{new_order_id}", json=new_order)

        resp = self.app.put(
            f"{BASE_URL}/{new_order_id}/cancel", json=new_order)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_order_not_exist(self):
        """It should not Cancel an non-existing Order"""
        # create an Order to cancel
        test_order = OrderFactory()
        resp = self.app.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # generate the request
        new_order = resp.get_json()
        new_order_id = new_order["id"] + 1

        resp = self.app.put(
            f"{BASE_URL}/{new_order_id}/cancel", json=new_order)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------

    def test_query_by_customer(self):
        """It should Query Orders by customer_id"""
        orders = self._create_orders(3)
        test_customer_id = orders[0].customer_id
        customer_id_count = len([order for order in orders if order.customer_id == test_customer_id])
        response = self.app.get(
            BASE_URL, query_string=f"customer_id={test_customer_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), customer_id_count)
        # check the data just to be sure
        for order in data:
            self.assertEqual(order["customer_id"], test_customer_id)

    def test_query_by_status(self):
        """It should Query Orders by status"""
        orders = self._create_orders(10)
        placed_orders = [order for order in orders if order.status == OrderStatus.PLACED]
        placed_count = len(placed_orders)
        logging.debug("Placed Orders [%d] %s", placed_count, placed_orders)

        # test for available
        response = self.app.get(BASE_URL, query_string="status=placed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), placed_count)
        # check the data just to be sure
        for order in data:
            self.assertEqual(order["status"], OrderStatus.PLACED.name)

    def test_query_orders_by_item(self):
        """It should Query Orders by product id of its including item"""
        orders = self._create_orders(3)
        order_1, order_2 = orders[0], orders[1]

        test_item_1 = {"id": 1, "order_id": order_1.id, "product_id": 11,
                       "quantity": 3, "price": 4}
        test_item_2 = {"id": 2, "order_id": order_2.id, "product_id": 11,
                       "quantity": 3, "price": 4}
        test_item_3 = {"id": 3, "order_id": order_2.id, "product_id": 22,
                       "quantity": 1, "price": 5}

        # add item product_id 11 to order_1
        resp = self.app.post(
            f"{BASE_URL}/{order_1.id}/items",
            json=test_item_1,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # add item product_id 11 to order_2
        resp = self.app.post(
            f"{BASE_URL}/{order_2.id}/items",
            json=test_item_2,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # add item product_id 22 to order_2
        resp = self.app.post(
            f"{BASE_URL}/{order_2.id}/items",
            json=test_item_3,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # test query item with id 1
        response = self.app.get(BASE_URL, query_string="product_id=11")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        logging.debug(data)
        self.assertEqual(len(data), 2)

    ######################################################################
    #  I T E M   T E S T   C A S E S
    ######################################################################

    def test_add_item(self):
        """It should Add an Item to an order"""
        order = self._create_orders(1)[0]
        item = ItemFactory()
        item.order_id = order.id
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["price"], item.price)

    def test_add_item_to_order_not_found(self):
        """It should not Add Items to the order that is not found"""
        item = ItemFactory()
        item.order_id = 0
        resp = self.app.post(
            f"{BASE_URL}/0/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item(self):
        """It should Get an Item from an order"""
        # create a known items
        order = self._create_orders(1)[0]
        item = ItemFactory()
        item.order_id = order.id
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # retrieve it back
        resp = self.app.get(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["price"], item.price)

    def test_get_item_list(self):
        """It should Get a list of Items"""
        # add two items to order
        order = self._create_orders(1)[0]
        item_list = ItemFactory.create_batch(2)
        item_list[0].order_id = order.id
        item_list[1].order_id = order.id
        # Create item 1
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[0].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create item 2
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[1].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.app.get(f"{BASE_URL}/{order.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_all_item_list(self):
        """It should Get a list of all Items"""
        all_orders = self._create_orders(2)
        # add two items to order 1
        order = all_orders[0]
        item_list = ItemFactory.create_batch(2)
        item_list[0].order_id = order.id
        item_list[1].order_id = order.id
        # Create item 1
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[0].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create item 2
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[1].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # add two items to order 2
        order = all_orders[1]
        item_list = ItemFactory.create_batch(2)
        item_list[0].order_id = order.id
        item_list[1].order_id = order.id
        # Create item 1
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[0].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create item 2
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[1].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.app.get(f"{ALL_ITEM_URL}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 4)

    def test_get_item_list_of_order_not_found(self):
        """It should not List Items of the order that is not found"""
        resp = self.app.get(f"{BASE_URL}/0/items")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        """It should Update an Item on an order"""
        # create a known item
        order = self._create_orders(1)[0]
        item = ItemFactory()
        item.order_id = order.id
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["product_id"] = 9999
        data["quantity"] = 8888
        data["price"] = 7777

        # send the update back
        resp = self.app.put(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        print(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.app.get(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        print("~~~~~~~~~~~~~~~~~~~~~~~~~", resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["product_id"], 9999)
        self.assertEqual(data["quantity"], 8888)
        self.assertEqual(data["price"], 7777)

    def test_update_item_not_found(self):
        """It should not Update an Item that is not found"""
        order = self._create_orders(1)[0]
        data = {}
        data["id"] = 10
        data["order_id"] = order.id
        data["product_id"] = 9999
        data["quantity"] = 8888
        data["price"] = 7777
        # item have not created yet
        resp = self.app.put(
            f"{BASE_URL}/{order.id}/items/10",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        """It should Delete an Item"""
        order = self._create_orders(1)[0]
        item = ItemFactory()
        item.order_id = order.id
        resp = self.app.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        resp = self.app.delete(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        resp = self.app.get(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
