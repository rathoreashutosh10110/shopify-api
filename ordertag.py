import time
import json
import requests
import shopify
import os
from datetime import datetime

shop_url = 'https://examcart.in/'
api_version = '2023-01'
private_app_password = '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'
session = shopify.Session(shop_url, api_version, private_app_password)
shopify.ShopifyResource.activate_session(session)

# Get all orders
query1 = '''
mutation addTags($id: ID!, $tags: [String!]!) {
  tagsAdd(id: $id, tags: $tags) {
    node {
      id
    }
    userErrors {
      message
    }
  }
}
'''

query = '''
query {
  orders(first: 10) {
    edges {
      node {
        id
        name
      }
    }
  }
}

'''
variable = {
  "id": "gid://shopify/Order/4976931242050",
  "tags": "one, two, three"
}


results = shopify.GraphQL().execute(query1, variable)
# print(json.dumps(results, indent=4))

# x = shopify.REST.Customer.search(
#     {
#         session: session,
#         query: 'phone:+919084964875'
#     }
# )

