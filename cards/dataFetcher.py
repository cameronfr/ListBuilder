import sqlite3
from functools import reduce
import itertools
from urllib.request import urlopen
import json
import re

#This class fetches data from a couple of general sources, and returns it in a standard format

conceptNetURIAPIString = "http://api.conceptnet.io/c/en/%s?filter=/c/en"
conceptNetGraphAPIString = "http://api.conceptnet.io/related/c/en/%s?filter=/c/en"
wikipediaAPIString = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles=%s&redirects"

def extractTextData(object):
    return extractDataFromWikipedia(object)

def extractDictionaryData(object):
    return None

def extractConceptnetAssociatons(object):
    object = "_".join(object.split())
    uri = object
    graphRequestString = conceptNetGraphAPIString  % uri
    response = json.loads(urlopen(graphRequestString).read().decode("utf8"))
    associations = []
    for assoc in response['related']:
        associations.append({"word": assoc['@id'].split('/')[-1], "score":float(assoc['weight'])})
    return associations

def extractConceptnetEdges(object):
    object = "_".join(object.split())
    uri = object
    graphRequestString = conceptNetGraphAPIString % uri
    response = json.loads(urlopen(graphRequestString).read().decode("utf8"))
    return response

def extractDataFromWikipedia(object):
    object = "_".join(object.split())
    requestString = wikipediaAPIString % object
    response = json.loads(urlopen(requestString).read().decode("utf8"))
    pages = response['query']['pages']
    firstpage = next (iter (pages.values()))
    text = firstpage['extract']

    #remove "sources" and "see also" sections
    text = re.sub(r'==\ See also[\S\s]*','',text)

    #remove section titles
    text = re.sub(r'=+[^=]{1,50}=+','',text)
    return text

#Left as an example for extracting from specfific data sources in the form of SQL databases
#
# def extractDataFromSQLDatabase(source,tokens,numRows):
#     conn = sqlite3.connect(source)
#     c = conn.cursor();
#     tokens = ["%"+token+"%" for token in tokens]
#     select = "SELECT * FROM food"
#     qualifier = "WHERE long_desc LIKE ?"
#     for i in range(len(tokens)-1):
#         qualifier = qualifier + " AND long_desc LIKE ?"
#     sqlCommand = select + " " + qualifier + " ORDER BY LENGTH(long_desc)"
#     print("extractDataFromSQLDatabase: statement is: <%s> with tokens: <%s>" % (sqlCommand,tokens) )
#     data = []
#     for row in itertools.islice(c.execute(sqlCommand,tuple(tokens)), numRows):
#         data.append(row)
#     [print(r) for r in data]
