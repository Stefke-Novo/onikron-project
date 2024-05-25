import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

CERT_FINGERPINT = "0F:4D:33:CB:A3:F4:74:B3:AB:EA:D1:48:D1:A7:CA:4B:CA:8C:38:0C:03:B7:35:B4:3F:7E:4F:54:E6:B5:41:94"
ELASTIC_PASSWORD= "y0_8ppm2XlshcSoqizyT"
class Search:
    def __init__(self):
        self.es = Elasticsearch(
            'https://localhost:9200',
            ssl_assert_fingerprint=("bff1685089a4264bf03971844639040101aa51424e5f295cf3a51b1fb7c824f3"),
            basic_auth=("elastic",ELASTIC_PASSWORD),
            http_compress=True) # <-- connection options need to be added here
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)