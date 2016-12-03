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
import nltk

#Make sure that the punkt dataset is available for NLP (used in article summarization)
nltk.download('punkt')

#Tag it with Noun Verb Object triples
nlpUrl = 'http://localhost:9000'

@app.route('/download/text')
def downloadText():
    url = request.args.get('url', '')
    if not url:
        return ''
    return downloadText(url)

def downloadText(url):
    article = download(url)
    return article.text

def download(url):
    article = Article(url=url, language='en')
    article.download()
    article.parse()
    return article

def summarize(url):
    article = download(url)
    article.nlp()
    return article.summary
    
@app.route('/parse/people')
#Split up parsing articles from parsing articles to speed up speach
def parsePeople():
    text = request.args.get('text', '')
    return json.dumps(parsePeople(text))

def parsePeople(text):
    #Only get NER annotations
    nounList = []
    try:
        resultJson = runNLP("tokenize,ssplit,ner", text)
        print(resultJson)
        for sentence in resultJson['sentences']:
            wholeNoun = ""
            for nerToken in sentence['tokens']:
                if (nerToken['ner'] == "PERSON" or nerToken['ner'] == "ORGANIZATION"):
                    wholeNoun += nerToken['word'] + " "
                else:
                    wholeNoun = wholeNoun.strip()
                    if (wholeNoun != ""):
                        nounList.append(wholeNoun)
                        print(wholeNoun)
                    wholeNoun = ""
        #Remove duplicate entries
        nounList = list(set(nounList))

    except ConnectionError as E:
        print(E)
    return nounList
    

@app.route('/parse/facts')
def parseFacts():
    url = request.args.get('url', '')
    facts = parseFacts(url)
    #print(facts)
    return json.dumps(facts)

def parseFacts(url):
    #Sentiment Annotators: "tokenize,ssplit,ner,depparse,openie,sentiment"
    sentenceTriples = {}
    try:
        resultJson = runNLP("tokenize,ssplit,ner,openie", summarize(url))
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
    except ConnectionError as E:
        print(E)
    return sentenceTriples

def runNLP(annotators, text):
    print("Querying CoreNLP with annotators: " + annotators + " and text: " + text)
    nlpParameters = {"annotators": annotators, "outputFormat": "json"}
    jsonEncodedParameters = json.dumps(nlpParameters)
    #Make sure text is utf8 to avoid international character issues
    nlpRequest = requests.post(nlpUrl + '/?properties=' + jsonEncodedParameters, data=text.encode('utf-8'))
    
    if ( nlpRequest.status_code == requests.codes.ok ):
        print("Query Succeeded - now processing")
        resultJson = json.loads(nlpRequest.text)
        #print(resultJson)
        return resultJson
    raise ConnectionError('Error contacting the Standford NLP Server' + str(nlpRequest.status_code) + '. Make sure it\'s running on localhost:9000')

if __name__ == '__main__':
    app.run()
