import xml.etree.ElementTree as ElementTree
from spacy.en import English
from cards import dataFetcher
from cards import queryParser
from collections import OrderedDict
from itertools import islice
from newspaper import Article
nlp = English()

#TODO: Encapsulate into a "Card" class

SIMILARITY_CUTOFF = 0.333

def generateCards(criteria, contentURL):
    data=[]

    print("Parsing Query: " + "criteria: " + str(criteria) + "  URL/URI: " + str(contentURL))
    parsedCriteria = queryParser.parseCriteria(criteria);

    isURL = "http://" in contentURL or "https://" in contentURL
    articleText = None
    if(isURL):
        article = Article(contentURL)
        article.download()
        article.parse()
        articleText = article.text
        articleText = nlp(articleText)
    else:
        print("Fetching Wikipedia text for parsed query: " + str(parsedCriteria))
        articleText = dataFetcher.extractTextData(contentURL)
        articleText = nlp(articleText,parse=True)

    for category in parsedCriteria['properties']:
        associations = dataFetcher.extractConceptnetAssociatons(category) + [{'word':category,'score':1}]
        print("Found ConceptNet associations for category {}: {}".format(category,[x['word'] for x in associations]))
        items = nlp_relevantSentences(articleText,associations)
        items = sorted(items, key=lambda item: item['score'], reverse=True)
        itemCard = {"title":category,'attributes':items[:12]}
        print("Finished card for category {}".format(category))
        data.append(itemCard)

    return data;

def nlp_relevantSentences(doc,subjects):
    for s in subjects:
        s['word'] = nlp(s['word'],parse=True)[0]
    bag = []
    for sent in doc.sents:
        score = 0
        for t in sent:
            for s in subjects:
                similarity = t.similarity(s['word'])
                if similarity > SIMILARITY_CUTOFF:
                    score += similarity*s['score']
        if score>0:
            bag.append({"sent":sent.text,"score":score})

    return bag

    #next steps: generalize the f(property, text). can do entity extraction (e.g. dates, names) on own. compare word vecs
