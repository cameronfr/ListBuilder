import json
import time
from random import random

#Parse a query string into an object(subject), and requested properties of said object.

defaultProperties =  ["purpose","usage","art","grow","war","country","size","person","definition","names"]

def parseQuery(query):
    #TODO: actual subject and properties / question extraction
    query = query.rstrip()
    object = query.rstrip().split(' ')[0]

    if len(query.split(' '))>1:
        properties = query.split(' ')[1:]
    else:
        properties = defaultProperties

    parsedQuery = {'object':object,'properties':properties}
    return parsedQuery
