import xml.etree.ElementTree as ElementTree
from spacy.en import English
from cards import dataFetcher
from cards import queryParser
from collections import OrderedDict
from itertools import islice
nlp = English()

#TODO: Encapsulate into a "Card" class

SIMILARITY_CUTOFF = 0.333

def generateCards(query):
    data=[]

    print("Parsing Query: " + str(query))
    parsedQuery = queryParser.parseQuery(query);

    print("Fetching Wikipedia text for parsed query: " + str(parsedQuery))
    wpText = dataFetcher.extractTextData(parsedQuery['object'])
    wpText = nlp(wpText,parse=True)
    for category in parsedQuery['properties']:
        associations = dataFetcher.extractConceptnetAssociatons(category) + [{'word':category,'score':1}]
        print("Found ConceptNet associations for category {}: {}".format(category,[x['word'] for x in associations]))
        items = nlp_relevantSentences(wpText,associations)
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
