import newspaper
from newspaper import Article
import sqlite3
from flask import Flask
from flask import request
app = Flask(__name__)
import re
import requests
import json
from corenlp_pywrap import pywrap as nlpWrap

@app.route('/download')
def download():
    url = request.args.get('url', '')
    if not url:
        return ''
    return download(url)

def download(url):
    article = Article(url=url)		#, language='en'
    article.download()
    article.parse()
    return article.text

@app.route('/parse')
def parse():
    url = request.args.get('url', '')
    return json.dumps(parse(url))

def parse(url):
    articleText = download(url)
    #Tag it with Noun Verb Object triples
    nlpUrl = 'http://localhost:9000'
    nlpParameters = {"annotators": "tokenize,ssplit,pos,lemma,ner,depparse,openie", "openie.resolve_coref": "true", "outputFormat": "json"}
    jsonEncodedParameters = json.dumps(nlpParameters)
    nlpRequest = requests.post(nlpUrl + '/?properties=' + jsonEncodedParameters, data=articleText[:800])
    
    if ( nlpRequest.status_code == requests.codes.ok ):
        resultJson = json.loads(nlpRequest.text)
        sentenceTriples = {}

        for sentence in resultJson['sentences']:
            for triple in sentence['openie']:
                subjectType = sentence['tokens'][triple['subjectSpan'][0]]['ner']
                objectType = sentence['tokens'][triple['objectSpan'][0]]['ner']
                triple['subjectType'] = subjectType
                triple['objectType'] = objectType

                if (subjectType == "PERSON" or subjectType == "ORGANIZATION" and 
                    objectType == "PERSON" or objectType == "ORGANIZATION" and
                    "'" not in triple['subject']):
                    #This is a good enough triple to consider
                    if sentence['index'] not in sentenceTriples.keys():
                        sentenceTriples[sentence['index']] = []    
                    sentenceTriples[sentence['index']].append(triple)
        return sentenceTriples
    return 'Error contacting the Standford NLP Server' + str(nlpRequest.status_code) + '. Make sure it\'s running on localhost:9000'

if __name__ == '__main__':
    app.run()
