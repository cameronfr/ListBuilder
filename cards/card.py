import xml.etree.ElementTree as ElementTree
from spacy.en import English
from cards import data as Data
nlp = English()
from collections import OrderedDict
from itertools import islice
#initialize all the connections in the beginning for speed, store them in an array or something

def generateCard(subject,cardType):
    print("generateCard: Generating card for object: <" + subject + "> and cardtype: <" + cardType + ">")
    data=[]

    #TEMPORARY PARSING
    if len(subject.split(' '))>1:
        testCategories = [subject.split(' ')[1]]
        subject = subject.split(' ')[0]
    else:
        testCategories = ["purpose","usage","art","grow","war","country","size","person","definition","names"]

    if(cardType == "Wikipedia_Parse"):
        wpText = Data.extractTextData(subject)
        wpText = nlp(wpText,parse=True)

        for category in testCategories:
            associations = Data._extractConceptnetAssociatons(category) + [{'word':category,'score':1}]
            items = nlp_relevantSentences(wpText,associations)
                #TODO: send cards as they are finished
            items = sorted(items, key=lambda item: item['score'], reverse=True)
            itemCard = {"title":category,'attributes':items[:12]}
            data.append(itemCard)

        dates = nlp_dates(wpText)
        sortedDates = OrderedDict(sorted(dates.items(), key=lambda t: t[1],reverse=True))
        sortedDatesCard = {'title':"Dates",'attributes':sortedDates}
        data.append(sortedDatesCard)

        peoples = nlp_people(wpText)
        peopleCard = {'title':"People",'attributes':peoples}
        data.append(peopleCard)

        bag = nlp_bagOfWords(wpText)
        sortedBag = OrderedDict(sorted(bag.items(), key=lambda t: t[1],reverse=True)[:15])
        simpleBagCard = {'title':"Bag of Words",'attributes':sortedBag}
        data.append(simpleBagCard)

    return data;
    #FOR DISPLAYING, FOR NOW JUST PASS A MAP OF ATTRIBUTES AND THEIR VALUES TO CSS, CAN CODE NICE LOOKING "WIDGETS" LATER
    #WHICH WOULD BE DEFINED IN THE CARD.xml->DISPLAY property

def nlp_relevantSentences(doc,subjects):
    for s in subjects:
        s['word'] = nlp(s['word'],parse=False)[0]
    bag = []
    for sent in doc.sents:
        score = 0
        for t in sent:
            for s in subjects:
                similarity = t.similarity(s['word'])
                if similarity > 0.8:
                    score += similarity*s['score']
        if score>0:
            bag.append({"sent":sent.text,"score":score})

    return bag

def nlp_bagOfWords(doc):
    bag = {}
    for t in doc:
        if (t.is_ascii and not t.is_digit and not t.is_punct and not t.is_space and not t.is_oov and not '=' in t.orth_ and not t.is_stop and not t.like_num and not t.orth_ == '\'s'):
            normalizedToken = t.lemma_.lower()
            if normalizedToken in bag:
                bag[normalizedToken] +=1
            else:
                bag[normalizedToken] = 1
    return bag

def nlp_dates(doc):
    bag = {}
    for sent in doc.sents:
        parsedSent = nlp(sent.text)
        for t in parsedSent.ents:
            if t.label_ == 'DATE':
                bag[t.orth_]=sent.text
                break
    return bag

def nlp_people(doc):
    bag = {}
    for sent in doc.sents:
        parsedSent = nlp(sent.text)
        for t in parsedSent.ents:
            if t.label_ == 'PERSON':
                bag[t.orth_]=sent.text
                break

    return bag

    #next steps: generalize the f(property, text). can do entity extraction (e.g. dates, names) on own. compare word vecs
