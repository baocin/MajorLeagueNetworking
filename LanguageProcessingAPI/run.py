import newspaper
from newspaper import Article
from flask import Flask
from flask import request
app = Flask(__name__)

import re
import requests
import json
from nltk.tokenize import sent_tokenize
from textstat.textstat import textstat
# from pynlg.lexicon.en import EnglishLexicon
# from pynlg.lexicon.feature.category import NOUN, VERB, DETERMINER
# from pynlg import make_noun_phrase
# import py4j.GatewayServer;

#Make sure that the punkt dataset is available for NLP (used in article summarization)
# print("Downloading Summarization Dataset")
# nltk.download('punkt')

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

def takeFirstNSentences(n, url):
    print("Getting sentences")
    text = downloadText(url)
    #sentenceDetector = nltk.data.load('tokenizers/punkt/english.pickle')
    splitSentences = sent_tokenize(text.strip())
    print(splitSentences)
    return '.'.join(splitSentences[0:3])

@app.route('/parse/people')
#Split up parsing articles from parsing articles to speed up speach
def parsePeople():
    text = request.args.get('text', '')
    return json.dumps(parsePeople(text))

def parsePeople(text):
    #Only get NER annotations
    nounList = []
    try:
        resultJson = runNLP({"annotators": "tokenize,ssplit,ner", "outputFormat": "json"}, text)
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
        #tokenize,ssplit,ner,openie
        #"openie.affinity_probability_cap": "0.75",
        # "openie.resolve_coref": "true", 
        #tokenize,ssplit,ner,pos,lemma,depparse,natlog,openie,coref
        resultJson = runNLP({"annotators": "tokenize,ssplit,ner,openie", "outputFormat": "json"}, downloadText(url))
        # print()
        # print(resultJson)
        # print()
        sentenceDictionary = {}
        for sentence in resultJson['sentences']:
            for triple in sentence['openie']:
                try:
                    subjectType = sentence['tokens'][triple['subjectSpan'][0]]['ner']
                    if (subjectType != "PERSON" and subjectType != "ORGANIZATION" ):
                        continue
                except Exception as E:
                    continue

                # objectType = sentence['tokens'][triple['objectSpan'][0]]['ner']
                # triple['subjectType'] = subjectType
                # triple['objectType'] = objectType

                # if (subjectType == "PERSON" or subjectType == "ORGANIZATION" and 
                #     objectType == "PERSON" or objectType == "ORGANIZATION" and
                #     "'" not in triple['subject']):
                    #This is a good enough triple to consider
                    # if sentence['index'] not in sentenceTriples.keys():
                        # sentenceTriples[sentence['index']] = []
                    
                newSentence = makeSentence(triple['object'], triple['relation'], triple['subject'])
                readingGradeLevel = textstat.flesch_kincaid_grade(newSentence)

                # test_data = newSentence
                # combinedGradeRange = [int(s) for s in re.findall(r'\d+', textstat.text_standard(newSentence)) ]
                # gradeLevel = textstat.flesch_kincaid_grade(newSentence)
                
                # metrics = [
                #     (textstat.flesch_kincaid_grade(test_data)), #8
                #     (textstat.flesch_reading_ease(test_data)),  #50 good, >60 bad
                #     (textstat.coleman_liau_index(test_data)),   #<15? >20 is bad
                #     (textstat.automated_readability_index(test_data)),  #<12 good, >12 bad
                #     (textstat.dale_chall_readability_score(test_data)), #13 good, 17 bad
                #     (textstat.difficult_words(test_data)),  #4 good, 6 bad
                #     (textstat.linsear_write_formula(test_data)),    #
                #     (textstat.gunning_fog(test_data)),  #28 
                #     combinedGradeRange[0]
                # ]
                
                # print(str(metrics))
                # print()
                if (readingGradeLevel >= 8):
                    if not triple['subject'] in sentenceDictionary:
                        sentenceDictionary[triple['subject']] = newSentence
                        sentences.append(newSentence)
                #input("")
    except ConnectionError as E:
        print(E)
    # except Exception as E:
    #     print(E)
    #     print("Couldn't parse url:" + url)
    #return sentenceTriples
    return sentences

def makeSentence(obj, verb, subject):
    #?subject=John&object=Sarah&verb=love
    print("Making sentence with " + obj + ", " + verb + ",  and " + subject)
    
    nlgRequest = requests.get(nlgUrl + '/nlg/makeSentence', params={'subject':subject, 'verb':verb, 'object':obj})
    if (nlgRequest.status_code == requests.codes.ok):
        print("Sentence Generated: " + nlgRequest.text)
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

def runNLP(nlpParameters, text):
    print("Querying CoreNLP with annotators: " + str(nlpParameters) + " and text: " + text) 
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
