"""
Item Steps

Steps file for Orders.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""


# import json
import requests
from behave import given
from compare import expect
# , ensure


@given(u'the following items')
def step_impl(context):
    """ create new items """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.get(
        context.BASE_URL + '/api/items')
    expect(context.resp.status_code).to_equal(200)

    for item in context.resp.json():
        context.resp = requests.delete(context.BASE_URL + '/api/orders/' + str(
            item["order_id"]) + '/items/' + str(item["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)

    for row in context.table:
        order_id = context.order_ids[int(row["order_id_index"])]
        # rest_endpoint = f"{context.BASE_URL}/orders/{int(row['order_id'])}/items"
        rest_endpoint = context.BASE_URL + "/api/orders/{}/items".format(order_id)
        # rest_endpoint = f"{context.BASE_URL}/orders/{int(order_id)}/items"
        payload = {
            "order_id": order_id,
            "product_id": int(row['product_id']),
            "quantity": int(row['quantity']),
            "price": float(row["price"])
        }
        context.resp = requests.post(rest_endpoint, json=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
    context.order_ids = list()
