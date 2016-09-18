import sqlite3
from functools import reduce
import itertools
from urllib.request import urlopen
import json
import re

#THIS CLASS GETS DATA FROM DATA SOURCES(APIS, DATABASES) AND DOES LITTLE PROCESSING
#SHOULD RETURN IN A STANDARD FORMAT, INDEPENDENT OF SOURCE
#SHOULD ONLY USE GENERAL SOURCES: WIKIPEDIA, DICTIONARY, WORDNET

#todo: catch exceptions, apply weights to all processes

def extractTextData(object):
    return extractDataFromWikipedia(object)

def extractDictionaryData(object):
    return None

def extractConceptnetAssociatons(object):
    object = "_".join(object.split())
    uriRequestString = "http://conceptnet5.media.mit.edu/data/5.4/uri?language=en&text=%s" % object
    uri = json.loads(urlopen(uriRequestString).read().decode("utf8"))['uri']
    graphRequestString = "http://conceptnet5.media.mit.edu/data/5.4/assoc%s?filter=/c/en/&limit=30" % uri
    response = json.loads(urlopen(graphRequestString).read().decode("utf8"))
    associations = []
    for assoc in response['similar']:
        associations.append({"word": assoc[0].split('/')[-1], "score":float(assoc[1])})
    return associations

def extractConceptnetEdges(object):
    object = "_".join(object.split())
    uriRequestString = "http://conceptnet5.media.mit.edu/data/5.4/uri?language=en&text=%s" % object
    uri = json.loads(urlopen(uriRequestString).read().decode("utf8"))['uri']
    graphRequestString = "http://conceptnet5.media.mit.edu/data/5.4/%s?filter=/c/en/" % uri
    response = json.loads(urlopen(graphRequestString).read().decode("utf8"))
    return response

def extractDataFromWikipedia(object):
    object = "_".join(object.split())
    #print (object)
    requestString = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles=%s&redirects" % object
    #print (requestString)
    response = json.loads(urlopen(requestString).read().decode("utf8"))
    pages = response['query']['pages']
    firstpage = next (iter (pages.values()))
    text = firstpage['extract']

    #remove "sources" and "see also" sections
    text = re.sub(r'==\ See also[\S\s]*','',text)

    #remove section titles
    text = re.sub(r'=+[^=]{1,50}=+','',text)
    return text

def extractDataFromSQLDatabase(source,tokens,numRows):
    conn = sqlite3.connect(source)
    c = conn.cursor();
    tokens = ["%"+token+"%" for token in tokens]
    select = "SELECT * FROM food"
    qualifier = "WHERE long_desc LIKE ?"
    for i in range(len(tokens)-1):
        qualifier = qualifier + " AND long_desc LIKE ?"
    sqlCommand = select + " " + qualifier + " ORDER BY LENGTH(long_desc)"
    print("extractDataFromSQLDatabase: statement is: <%s> with tokens: <%s>" % (sqlCommand,tokens) )
    data = []
    for row in itertools.islice(c.execute(sqlCommand,tuple(tokens)), numRows):
        data.append(row)
    [print(r) for r in data]
