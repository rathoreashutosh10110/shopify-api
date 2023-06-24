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

query = '''
{
  customers(first: 1, query:"phone:+919084964875") {
    edges {
      node {
        firstName
        phone
        email
        id
        
        orders(first: 4) {
            edges {
                node {
                    id
                    name
                    createdAt 
                    phone
                    subtotalPrice
                }
            }
        }
      }
    }
  }
}
'''

query2 = '''
{
    customers: {
    id: "6076484911170",
    password: "ashutosh123",
    password_confirmation: "ashutosh123"
    }
}
'''

results = shopify.GraphQL().execute(query)
print(results)