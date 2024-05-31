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
    from_ = request.form.get('from_', type=int, default=0)
    results = es.search(
        query={
        #    'bool':{
        #         'should':{
        #             'match':{
        #                 "contents":{
        #                     'query': query
        #                 }
        #             },
        #             'match':{
        #                 "title":{
        #                     'query': query
        #                 }
        #             }
        #         }
        #     }
            # 'multi_match':{
            #     'query':query,
            #     'fields': ['title','contents']
            # }

            'multi_match':{
                'query':query,
                'fields': ['customer_first_name','customer_last_name']
            }
        },
        aggs={
            'first-agg':{
                'terms':{
                    'field':'category.keyword'
                }
            }
        },
        size=5,
        from_=from_
    )
    # pprint(results)
    return render_template('index.html', results=results['hits']['hits'],
                           query=query, from_=0,
                           total=results['hits']['total']['value'],
                           aggs={
                                    'Category': {
                                        bucket['key']: bucket['doc_count']
                                        for bucket in results['aggregations']['first-agg']['buckets']
                                    },
                                })


@app.get('/document/<id>')
def get_document(id):
    document = es.retrieve_document(id)
    title = document['_source']['title']
    paragraphs = document['_source']['contents'].split('\n')
    return render_template('document.html', title=title, paragraphs=paragraphs)

@app.cli.command()
def make_index():
    es.build_index()

@app.cli.command()
def add_document():
    es.create_document()
