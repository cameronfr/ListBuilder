import json
import time
from random import random

#Parse a query string into an object(subject), and requested properties of said object.

defaultProperties =  ["purpose","usage","art","grow","war","country","size","person","definition","names"]

def parseCriteria(criteria):
    #TODO: actual subject and properties / question extraction
    print(criteria)
    criteria = criteria.rstrip()
    object = criteria.rstrip().split(' ')[0]

    if len(criteria.split(' '))>0:
        properties = criteria.split(' ')[0:]
    else:
        properties = defaultProperties

    parsedCriteria = {'properties':properties}
    return parsedCriteria
