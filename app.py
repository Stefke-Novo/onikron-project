from pprint import pprint
import re
from flask import Flask, render_template, request
from search import Search

app = Flask(__name__)
es = Search()

@app.get('/')
def index():
    return render_template('index.html')


@app.post('/')
def handle_search():
    query = request.form.get('query', '')
    results = es.search(
        query={
           'bool':{
                'should':{
                    'match':{
                        "contents":{
                            'query': query
                        }
                    },
                    'match':{
                        "title":{
                            'query': query
                        }
                    }
                }
            }
        }
    )
    pprint(results)
    return render_template('index.html', results=results['hits']['hits'],
                           query=query, from_=0,
                           total=results['hits']['total']['value'])


@app.get('/document/<id>')
def get_document(id):
    return 'Document not found'

@app.cli.command()
def make_index():
    es.build_index()

@app.cli.command()
def add_document():
    es.create_document()
