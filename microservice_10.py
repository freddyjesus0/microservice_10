#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request #import main Flask class and request object
import pika 
import MySQLdb
import json
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#from urlparse import parse_qs
import cgi
import boto3
import os


app = Flask(__name__)
@app.route('/microservicio/consultaproductosproveedor', methods=['GET'])
def consulta_producto_proveedor():

    if request.method == "GET":
            
        try:

            dynamodb = boto3.client('dynamodb',aws_access_key_id=os.environ.get('aws_access_key_id'), aws_secret_access_key=os.environ.get('aws_access_key_secret'), region_name=os.environ.get('region'))
            #dynamodb = boto3.client('dynamodb',aws_access_key_id="AKIAIQCRHLBZV3V555MQ", aws_secret_access_key="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", region_name="us-east-1") 

            proveedor_id = request.args.get('id_proveedor')
            #product = dynamodb.get_item(
            #        TableName = "Product_Read",
            #        Key= { "id_producto": {"N": str(product_id) } }
            #)

            response = dynamodb.scan(
                TableName = "Product_Read",
            )
            
            linked_items = []
            items = response['Items']
            #print(items)
            #categoria = product['Item']['categoria']['S']

            for item in items:
                if item['id_proveedor']['S'] == proveedor_id:
                    linked_items.append(item)
                   
            
            return  json.dumps(linked_items)

        except:
            return  json.dumps({'msg': "No hay productos asociados al proveedor"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5009)
