import newspaper
from newspaper import Article
import sqlite3
from flask import Flask
from flask import request
app = Flask(__name__)
import nltk
from nltk.tag import StanfordNERTagger
import re
import pprint

@app.route("/download")
def download():
    url = request.args.get('url', '')
    return download(url)

def download(url):
    article = Article(url=url)		#, language='en'
    article.download()
    article.parse()
    return article.text

@app.route("/parse")
def parse():
    url = request.args.get('url', '')
    return parse(url)

def parse(url):
    articleText = download(url)
    tagger = StanfordNERTagger('stanford-ner/english.all.3class.nodistsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
    return str(tagger.tag(articleText.split()))

    # tagged_sentences = ie_preprocess(articleText)
    # chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
    # entity_names = []
    # for tree in chunked_sentences:
    #     # Print results per sentence
    #     # print(extract_entity_names(tree))
    #     entity_names.extend(extract_entity_names(tree))
    # return str(entity_names)

def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        # return t + "/" + t.label
        # print(t.label())
        # print(t)
        # entity_names.append(' '.join([child[0] for child in t]) + "/" + t.label)
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    return entity_names

# 	from nltk.tag.stanford import NERTagger
# st = NERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
# text = """YOUR TEXT GOES HERE"""
#
# for sent in nltk.sent_tokenize(text):
#     tokens = nltk.tokenize.word_tokenize(sent)
#     tags = st.tag(tokens)
#     for tag in tags:
#         if tag[1]=='PERSON': print tag
#
# #Probable categoried we want to focus on
# # categories = ['nfl', 'nbz','mlb','ncaab','nhl']
#
#
# #All the websites we want to scan
# espn_paper = newspaper.build('http://www.espn.com/', memoize_articles=False)
# # foxnews_paper = newspaper.build('http://www.foxsports.com/')
# # sportingnews_paper = newspaper.build('http://www.sportingnews.com/')		#
#
# #Multithread the downloads
# papers = [espn_paper]		#, foxnews_paper, sportingnews_paper
# # news_pool.set(papers, threads_per_source=4)
# # news_pool.join()		#Wait until all are done
#
#
# #The source brand and description
# for paper in papers:
# 	print(paper.brand)
# 	print(paper.description)
# 	print(paper.size())
# 	for article in paper.articles:
# 		print('\t', article.url)
# 		#Download must be called before parsing
# 		article.download()
# 		article.parse()
# 		print('\t\t', article.title)
# 		# article.authors
# 		# article.text
# 		# article.top_image
#
#
#
# # for category in espn.category_urls():
# # 	print(category)
# # 	section = newspaper.build(category )
#
# # for article in espn.articles:
# # 	print(article.url)
#
if __name__ == "__main__":
    app.run()
