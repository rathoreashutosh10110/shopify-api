import time
import json
import requests
import shopify
import os
import mysql.connector
from datetime import datetime


    
affiliate_db_params = {
    'host': '103.174.54.87',
    'user': 'ravigarg',
    'database': 'affiliate',
    'password': 'R@vig@rg1907',
    'port': '3306'
}

update_sql = '''INSERT INTO affiliateapp_order (order_id, order_status, order_date, order_amount, order_discount_code, buyer_name, order_quantity, payment_status, payment_gateway)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    order_status = VALUES(order_status),
    order_date = VALUES(order_date),
    order_amount = VALUES(order_amount),
    order_discount_code = VALUES(order_discount_code),
    buyer_name = VALUES(buyer_name),
    order_quantity = VALUES(order_quantity),
    payment_status = VALUES(payment_status),
    payment_gateway = VALUES(payment_gateway)
'''

conn = mysql.connector.connect(**affiliate_db_params)
cur = conn.cursor()
while True:
  try:
    coupon_codes = []

    cur.execute("SELECT DISTINCT discount_code FROM affiliateapp_teacher")
    discount_codes = cur.fetchall()
    print(discount_codes)
    shop_url = 'https://examcart.in/'
    api_version = '2023-01'
    private_app_password = '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'
    session = shopify.Session(shop_url, api_version, private_app_password)
    shopify.ShopifyResource.activate_session(session)

    for code in discount_codes:
        coupon_codes.append(code[0])


    for code in coupon_codes:
      if code == 'DISCOUNT':
        continue
      
      inital_bulk_query = '''
      mutation {
        bulkOperationRunQuery(
          query:"""
          query {
        orders(query: "discount_code:{coupon_code}") {
          edges {
            node {
              id
              name
              createdAt
              totalPriceSet {
                presentmentMoney {
                  amount
                }
              }
              displayFulfillmentStatus
              customer{
                displayName
              }
              subtotalLineItemsQuantity
              displayFinancialStatus
              paymentGatewayNames
              totalShippingPriceSet{
                presentmentMoney{
                  amount
                }
              }
            }
          }
        }
      }
      """
      ) {
          bulkOperation {
            id
            status
          }
          userErrors {
            field
            message
          }
        }
      }
      '''
      final_bulk_query = inital_bulk_query.replace('{coupon_code}', code)
      print(code)
      result1 = shopify.GraphQL().execute(final_bulk_query)
      time.sleep(2)
      print("resutl1", result1)
      json_data = json.loads(result1)
      id = json_data.get('data').get(
          'bulkOperationRunQuery').get('bulkOperation').get('id')

      query2 = '''
      {
        node(id:"{idfinal}") {
          ... on BulkOperation {
            id
            status
            errorCode
            createdAt
            completedAt
            objectCount
            fileSize
            url
            partialDataUrl
          }
        }
      }

      '''
      query2 = query2.replace('{idfinal}', id)
      recieved = False
      while not recieved:
        print(code)
        try:
          result2 = shopify.GraphQL().execute(query2)
        except:
          print("error")
          continue
        json_data2 = json.loads(result2)
        if json_data2.get('data').get('node').get('status') == 'COMPLETED':
          recieved = True
        else:
          time.sleep(2)
          print("waiting for response")
          continue
      url = json_data2.get('data').get('node').get('url')
      print("url", url)

      if url is None:
        continue

      response = requests.get(url, stream=True, allow_redirects=True)
      # r = requests.get(url, allow_redirects=True)
      print("recieved response")
      # open('Code Data.txt', 'wb').write(r.content)
      for line in response.iter_lines():
        if not line:
            continue
        decoded_line = line.decode('utf-8')
        json_obj = json.loads(decoded_line)
        order_id = json_obj.get('name')
        order_status = json_obj.get('displayFulfillmentStatus')
        order_date = datetime.fromisoformat(json_obj.get('createdAt').replace('Z', '+00:00'))
        order_amount = float(json_obj.get('totalPriceSet').get('presentmentMoney').get('amount')) - float(json_obj.get('totalShippingPriceSet').get('presentmentMoney').get('amount'))
        order_discount_code = code
        buyer_name = json_obj.get('customer').get('displayName')
        order_quantity = json_obj.get('subtotalLineItemsQuantity')
        payment_status = json_obj.get('displayFinancialStatus')
        try:
          payment_gateway = json_obj.get('paymentGatewayNames')[0]
        except:
          payment_gateway = "None"
        cur.execute(update_sql, (order_id, order_status, order_date, order_amount, order_discount_code, buyer_name, order_quantity, payment_status, payment_gateway))
        conn.commit()
    shopify.ShopifyResource.clear_session()
  except Exception as e:
    print(e)
    print("error")
    continue
      
      





