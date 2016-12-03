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
# from pynlg.lexicon.en import EnglishLexicon
# from pynlg.lexicon.feature.category import NOUN, VERB, DETERMINER
# from pynlg import make_noun_phrase
# import py4j.GatewayServer;

#Make sure that the punkt dataset is available for NLP (used in article summarization)
print("Downloading Summarization Dataset")
nltk.download('punkt')

#Tag it with Noun Verb Object triples
nlpUrl = 'http://localhost:9000'
nlgUrl = 'http://localhost:9090'

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
    print("Downloading " + url)
    article = Article(url=url, language='en')
    article.download()
    article.parse()
    return article

def summarize(url):
    print("Summarizing " + url)
    article = Article(url=url, language='en')
    article.download()
    article.parse()
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
    # sentenceTriples = {}
    sentences = []
    try:
        resultJson = runNLP("tokenize,ssplit,ner,openie", summarize(url))
        # print()
        # print(resultJson)
        # print()
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
                    # if sentence['index'] not in sentenceTriples.keys():
                        # sentenceTriples[sentence['index']] = []
                    
                    sentence = makeSentence(triple['object'], triple['relation'], triple['subject'])
                    print("Sentence:" + sentence)
                    # sentenceTriples[sentence['index']].append(triple)
                    sentences.append(sentence)
    except ConnectionError as E:
        print(E)
    except Exception as E:
        print("Couldn't parse url:" + url)
    #return sentenceTriples
    return sentences

def makeSentence(obj, verb, subject):
    #?subject=John&object=Sarah&verb=love
    print("Making sentence with " + obj + ", " + verb + ",  and " + subject);
    
    nlgRequest = requests.get(nlgUrl + '/nlg/makeSentence', params={'subject':subject, 'verb':verb, 'object':obj})
    if (nlgRequest.status_code == requests.codes.ok):
        print("Sentence Generation Succeeded - " + nlgRequest.text)
        return nlgRequest.text
    return ""
    # lex = EnglishLexicon()
    # noun = lex.first(obj, category=NOUN)
    # verb = lex.first(verb, category=VERB)
    # subject = lex.first(subject, category=NOUN)
    # # beau = lex.first(u'beau', category=ADJECTIVE)
    # # perdu = lex.first(u'perdu', category=ADJECTIVE)
    # phrase = make_noun_phrase(lexicon=lex, specifier=noun, noun=subject)
    # syntaxically_realised_phrase = phrase.realise()
    # #morphologically_realised_phrase = syntaxically_realised_phrase.realise_morphology()
    # return syntaxically_realised_phrase

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
