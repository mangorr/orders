"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, make_response, abort
from service.models import Order, Item, OrderStatus
from .utils import status  # HTTP Status CodesS

# Import Flask application
from . import app


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


# ---------------------------------------------------------------------
#                O R D E R   M E T H O D S
# ---------------------------------------------------------------------
######################################################################
# LIST ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """Returns all of the Orders"""
    app.logger.info("Request for order list")

    orders = []
    customer_id = request.args.get("customer_id")
    order_status = request.args.get("status")
    product_id = request.args.get("product_id")
    if customer_id:
        app.logger.info("Find by customer id: %s", customer_id)
        orders = Order.find_by_customer(int(customer_id))
    elif order_status:
        app.logger.info("Find by status: %s", status)
        # create enum from string
        status_value = getattr(OrderStatus, order_status.upper())
        orders = Order.find_by_status(status_value)
    elif product_id:
        app.logger.info("Find by items: %s", product_id)
        orders = Order.find_by_item(int(product_id))
    else:
        app.logger.info("Find all")
        orders = Order.all()

    results = [order.serialize() for order in orders]
    app.logger.info("[%s] Orders returned", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# CREATE A NEW ORDER
######################################################################


@app.route("/orders", methods=["POST"])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    app.logger.info("Request to create an Order")
    check_content_type("application/json")
    order = Order()
    order.deserialize(request.get_json())
    order.create()
    message = order.serialize()
    location_url = url_for("get_orders", order_id=order.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_orders(order_id):
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

    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_orders(order_id):
    """
    Update an Order

    This endpoint will update an Order based the body that is posted
    """
    app.logger.info("Request to update Order with id: %s", order_id)
    check_content_type("application/json")
    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' was not found."
        )

    order.deserialize(request.get_json())
    order.id = order_id
    order.update()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE AN ORDER
######################################################################


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_orders(order_id):
    """
    Delete an Order

    This endpoint will delete an Order based the id specified in the path
    """
    app.logger.info("Request to delete order with id: %s", order_id)
    order = Order.find(order_id)
    if order:
        order.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# CANCEL AN ORDER
######################################################################


@app.route("/orders/<int:order_id>/cancel", methods=["PUT"])
def cancel_orders(order_id):
    """
    Cancel an Order

    This endpoint will cancel an Order based the body that is posted
    """
    app.logger.info("Request to cancel Order with id: %s", order_id)
    check_content_type("application/json")
    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' was not found."
        )
    print(order)
    # Check if the order can be cancelled
    if order.status in [OrderStatus.DELIVERED, OrderStatus.SHIPPED]:
        abort(
            status.HTTP_400_BAD_REQUEST,
            f"Order with id '{order_id}' cannot be cancelled."
        )

    order.status = OrderStatus.CANCELLED
    order.id = order_id
    order.update()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


# ---------------------------------------------------------------------
#                I T E M   M E T H O D S
# ---------------------------------------------------------------------
######################################################################
# LIST ITEMS FOR AN ORDER
######################################################################
@app.route("/orders/<int:order_id>/items", methods=["GET"])
def list_items(order_id):
    """Returns all of the Items for an order"""
    app.logger.info("Request for all Items for Order with id: %s", order_id)

    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' could not be found.",
        )

    results = [item.serialize() for item in order.order_items]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# ADD AN ITEM TO AN ORDER
######################################################################
@app.route("/orders/<int:order_id>/items", methods=["POST"])
def create_items(order_id):
    """
    Create an Item on an Order

    This endpoint will add an item to an order
    """
    app.logger.info("Request to create an Item for Order with id: %s", order_id)
    check_content_type("application/json")

    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' could not be found.",
        )

    item = Item()
    item.deserialize(request.get_json())
    order.order_items.append(item)
    order.update()
    message = item.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)


######################################################################
# UPDATE AN ITEM
######################################################################
@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["PUT"])
def update_items(order_id, item_id):
    """
    Update an Item

    This endpoint will update an Item based the body that is posted
    """
    app.logger.info(
        "Request to update Item %s for Order id: %s", (item_id, order_id)
    )
    check_content_type("application/json")

    item = Item.find(item_id)

    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{item_id}' could not be found.",
        )

    item.deserialize(request.get_json())
    item.id = item_id
    item.update()

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN ITEM FROM ORDER
######################################################################
@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["GET"])
def get_items(order_id, item_id):
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

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ITEM
######################################################################
@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(order_id, item_id):
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

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}"
    )
