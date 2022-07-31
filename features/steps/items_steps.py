"""
Item Steps

Steps file for Orders.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""


import json
import requests
from behave import *
from compare import expect, ensure


@given(u'the following items')
def step_impl(context):
    """ create new items """
    
    headers = {'Content-Type': 'application/json'}
    for row in context.table:
        # print(row)
        rest_endpoint = f"{context.BASE_URL}/orders/{int(row['order_id'])}/items"
        # rest_endpoint = context.BASE_URL + "/orders/{}/items".format(row[0])
        payload = {
            "order_id": int(row['order_id']),
            "product_id": int(row['product_id']),
            "quantity": int(row['quantity']),
            "price": float(row["price"])
        }
        context.resp = requests.post(rest_endpoint, data=payload, headers= headers)
        expect(context.resp.status_code).to_equal(201)
    context.order_id = list()