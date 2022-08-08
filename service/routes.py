"""
Order Service with Swagger
Paths:
------
index             GET      /

list_orders     GET      /orders
create_orders   POST     /orders
get_orders      GET      /orders/<int:order_id>
update_orders   PUT      /orders/<int:order_id>
delete_orders   DELETE   /orders/<int:order_id>

list_items    GET      /orders/<int:order_id>/items
create_items  POST     /orders/<int:order_id>/items
get_items     GET      /orders/<int:order_id>/items/<int:item_id>
update_items  PUT      /orders/<int:order_id>/items/<int:item_id>
delete_items  DELETE   /orders/<int:order_id>/items/<int:item_id>
"""

from flask import jsonify, make_response
from service.models import Order, Item, OrderStatus
from flask_restx import Resource, fields, reqparse
from .utils import status  # HTTP Status CodesS

# Import Flask application
from . import app, api


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="OK"), status.HTTP_200_OK)


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


create_order_model = api.model('Order', {
    'customer_id': fields.Integer(required=True,
                                  description='The Customer ID of the order'),
    'tracking_id': fields.Integer(required=True,
                                  description='The Tracking ID of the order'),
    'status': fields. String(enum=OrderStatus._member_names_, description='The Status of the order'),
})

order_model = api.inherit(
    'OrderModel',
    create_order_model,
    {
        'id': fields.Integer(readOnly=True,
                             description='The unique ID assigned internally by service'),
        'created_time': fields.Date(required=True,
                                    description='The Created Time of the order'),
        'order_items': fields.Raw(required=True,
                                  description='The Items of the order'),
    }
)

create_item_model = api.model('Item', {
    'order_id': fields.Integer(required=True,
                               description='The Order ID of the item'),
    'product_id': fields.Integer(required=True,
                                 description='The Product ID of the item'),
    'quantity': fields.Integer(required=True,
                               description='The Quantity of the item'),
    'price': fields.Float(required=True,
                          description='The Price of the item')
})

item_model = api.inherit(
    'ItemModel',
    create_item_model,
    {
        'id': fields.Integer(readOnly=True,
                             description='The unique ID assigned internally by service')
    }
)

# query string arguments
order_args = reqparse.RequestParser()
order_args.add_argument('customer_id', type=int, required=False, help='List Orders by customer_id')
order_args.add_argument('status', type=str, required=False, help='List Orders by status')
order_args.add_argument('product_id', type=int, required=False, help='List Orders by Item\'s product_id')


# ---------------------------------------------------------------------
#                O R D E R   M E T H O D S
# ---------------------------------------------------------------------
######################################################################
# PATH: /orders/{order_id}
######################################################################
@api.route('/orders/<int:order_id>')
@api.param('order_id', 'The Order identifier')
class OrderResource(Resource):
    """
    OrderResource class
    Allows the manipulation of an Order
    GET /order{id} - Returns an Order with the id
    PUT /order{id} - Updates an Order with the id
    DELETE /order{id} -  Deletes an Order with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('get_orders')
    @api.response(404, 'Order not found')
    @api.marshal_with(order_model)
    def get(self, order_id):
        """
        Retrieve a single Order

        This endpoint will return an Order based on it's id
        """
        app.logger.info("Request for Order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' could not be found.",
            )
        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ORDER
    # ------------------------------------------------------------------
    @api.doc('update_orders')
    @api.response(404, 'Order not found')
    @api.response(400, 'The posted Order data was not valid')
    @api.expect(order_model)
    @api.marshal_with(order_model)
    def put(self, order_id):
        """
        Update an Order

        This endpoint will update an Order based the body that is posted
        """
        app.logger.info("Request to update Order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' was not found."
            )
        app.logger.debug('Payload = %s', api.payload)
        order.deserialize(api.payload)
        order.id = order_id
        order.update()
        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('delete_orders')
    @api.response(204, 'Order deleted')
    def delete(self, order_id):
        """
        Delete an Order

        This endpoint will delete an Order based the id specified in the path
        """
        app.logger.info("Request to delete order with id: %s", order_id)
        order = Order.find(order_id)
        if order:
            order.delete()
            app.logger.info('Order with id [%s] was deleted', order_id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders
######################################################################
@api.route('/orders', strict_slashes=False)
class OrderCollection(Resource):
    """ Handles all interactions with collections of Orders """
    # ------------------------------------------------------------------
    # LIST ALL ORDERS
    # ------------------------------------------------------------------
    @api.doc('list_orders')
    @api.expect(order_args, validate=True)
    @api.marshal_list_with(order_model)
    def get(self):
        """Returns all of the Orders"""
        app.logger.info("Request for order list")
        orders = []
        args = order_args.parse_args()
        if args["customer_id"]:
            app.logger.info("Find by customer id: %s", args["customer_id"])
            orders = Order.find_by_customer(args["customer_id"])
        elif args["status"]:
            app.logger.info("Find by status: %s", args["status"])
            # create enum from string
            orders = Order.find_by_status(args["status"].upper())
        elif args["product_id"]:
            app.logger.info("Find by items: %s", args["product_id"])
            orders = Order.find_by_item(args["product_id"])
        else:
            app.logger.info("Find all")
            orders = Order.all()

        results = [order.serialize() for order in orders]
        app.logger.info("[%s] Orders returned", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ORDER
    # ------------------------------------------------------------------
    @api.doc('create_orders')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_order_model)
    @api.marshal_with(order_model, code=201)
    def post(self):
        """
        Creates an Order
        This endpoint will create an Order based the data in the body that is posted
        """
        app.logger.info("Request to create an Order")
        order = Order()
        app.logger.debug('Payload = %s', api.payload)
        order.deserialize(api.payload)
        order.create()
        app.logger.info('Order with new id [%s] created!', order.id)
        location_url = api.url_for(OrderResource, order_id=order.id, _external=True)
        return order.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /orders/{order_id}/cancel
######################################################################
@api.route('/orders/<int:order_id>/cancel')
@api.param('order_id', 'The Order identifier')
class CancelResource(Resource):
    """ Cancel actions on an Order """
    @api.doc('cancel_orders')
    @api.response(404, 'Order not found')
    @api.response(400, 'The Order cannot be cancelled')
    @api.marshal_with(order_model)
    def put(self, order_id):
        """
        Cancel an Order

        This endpoint will cancel an Order based the body that is posted
        """
        app.logger.info("Request to cancel Order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' was not found."
            )
        # Check if the order can be cancelled
        if order.status in [OrderStatus.DELIVERED, OrderStatus.SHIPPED]:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Order with id '{order_id}' cannot be cancelled."
            )

        order.status = OrderStatus.CANCELLED
        order.id = order_id
        order.update()
        app.logger.info('Order with id [%s] has been cancelled!', order.id)
        print("here!")
        return order.serialize(), status.HTTP_200_OK


# ---------------------------------------------------------------------
#                I T E M   M E T H O D S
# ---------------------------------------------------------------------
######################################################################
# PATH: /orders/{order_id}/items/{item_id}
######################################################################
@api.route('/orders/<int:order_id>/items/<int:item_id>')
@api.param('order_id', 'The Order identifier')
@api.param('item_id', 'The Item identifier')
class ItemResource(Resource):
    """
    ItemResource class
    Allows the manipulation of an Item
    GET /item{id} - Returns an Item with the id
    PUT /item{id} - Updates an Item with the id
    DELETE /item{id} -  Deletes an Item with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ITEM FROM ORDER
    # ------------------------------------------------------------------
    @api.doc('get_items')
    @api.response(404, 'Item not found')
    @api.marshal_with(item_model)
    def get(self, order_id, item_id):
        """
        Get an Item
        This endpoint returns just an item
        """
        app.logger.info(
            "Request to retrieve Item %s for Order id: %s", item_id, order_id
        )

        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Item with id '{item_id}' could not be found.",
            )
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ORDER
    # ------------------------------------------------------------------
    @api.doc('update_items')
    @api.response(404, 'Item not found')
    @api.response(400, 'The posted Item data was not valid')
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, order_id, item_id):
        """
        Update an Item
        This endpoint will update an Item based the body that is posted
        """
        app.logger.info(
            "Request to update Item %s for Order id: %s", (item_id, order_id)
        )
        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{item_id}' could not be found.",
            )

        app.logger.debug('Payload = %s', api.payload)
        item.deserialize(api.payload)
        item.id = item_id
        item.update()
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('delete_items')
    @api.response(204, 'Item deleted')
    def delete(self, order_id, item_id):
        """
        Delete an Item
        This endpoint will delete an Item based the id specified in the path
        """
        app.logger.info(
            "Request to delete Item %s for Order id: %s", (item_id, order_id)
        )
        item = Item.find(item_id)
        if item:
            item.delete()
            app.logger.info('Item with id [%s] was deleted', item_id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders/{order_id}/items
######################################################################
@api.route('/orders/<int:order_id>/items', strict_slashes=False)
class ItemCollection(Resource):
    """ Handles all interactions with collections of Items """
    # ------------------------------------------------------------------
    # LIST ITEMS FOR AN ORDER
    # ------------------------------------------------------------------
    @api.doc('list_items')
    @api.response(404, 'Order not found')
    @api.marshal_list_with(order_model)
    def get(self, order_id):
        """Returns all of the Items for an order"""
        app.logger.info("Request for all Items for Order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' could not be found.",
            )

        results = [item.serialize() for item in order.order_items]
        app.logger.info("[%s] Items returned", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD AN ITEM TO AN ORDER
    # ------------------------------------------------------------------
    @api.doc('create_items')
    @api.response(400, 'The posted data was not valid')
    @api.response(404, 'Order not found')
    @api.expect(create_item_model)
    @api.marshal_with(item_model, code=201)
    def post(self, order_id):
        """
        Create an Item on an Order
        This endpoint will add an item to an order
        """
        app.logger.info("Request to create an Item for Order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' could not be found.",
            )

        item = Item()
        app.logger.debug('Payload = %s', api.payload)
        item.deserialize(api.payload)
        order.order_items.append(item)
        order.update()
        return item.serialize(), status.HTTP_201_CREATED


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
