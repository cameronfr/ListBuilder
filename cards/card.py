import xml.etree.ElementTree as ElementTree
from spacy.en import English
from cards import dataFetcher
from cards import queryParser
from collections import OrderedDict
from itertools import islice
nlp = English()

#TODO: Encapsulate into a "Card" class

def generateCards(query):
    data=[]

    parsedQuery = queryParser.parseQuery(query);
    print(parsedQuery)

    wpText = dataFetcher.extractTextData(parsedQuery['object'])
    wpText = nlp(wpText,parse=True)
    for category in parsedQuery['properties']:
        associations = dataFetcher.extractConceptnetAssociatons(category) + [{'word':category,'score':1}]
        items = nlp_relevantSentences(wpText,associations)
        items = sorted(items, key=lambda item: item['score'], reverse=True)
        itemCard = {"title":category,'attributes':items[:12]}
        print(itemCard);
        data.append(itemCard)

    return data;

def nlp_relevantSentences(doc,subjects):
    print(subjects)
    for s in subjects:
        s['word'] = nlp(s['word'],parse=True)[0]
    bag = []
    for sent in doc.sents:
        score = 0
        for t in sent:
            for s in subjects:
                similarity = t.similarity(s['word'])
                if similarity > 0.7:
                    score += similarity*s['score']
        if score>0:
            bag.append({"sent":sent.text,"score":score})

    return bag

    #next steps: generalize the f(property, text). can do entity extraction (e.g. dates, names) on own. compare word vecs
