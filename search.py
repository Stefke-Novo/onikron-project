import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from flask import app

load_dotenv()

ELASTIC_PASSWORD= "0_TtDyV0V7lW3U*yM+Mq"
class Search:
    def __init__(self):
        self.es = Elasticsearch(
            'https://localhost:9200',
            ssl_assert_fingerprint=("4963d0ec08ff37859e0211405a5b5642330307c794d4dc27074274907113328a"),
            basic_auth=("elastic",ELASTIC_PASSWORD),
            http_compress=True) # <-- connection options need to be added here
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def build_index(self):
        self.es.indices.create(index="my_documents")

    def search(self, **query_args):
        return self.es.search(index='my_documents', **query_args)
    
    def print_message():
        print("First message is printed")

    def create_document(self):
        document = {
            'title': 'Work From Home Policy',
            'contents': 'The purpose of this full-time work-from-home policy is...',
            'created_on': '2023-11-02',
        }
        response = self.es.index(index='my_documents', body=document)
        print(response['_id'])
