import json
import time
from random import random

#Get the types of cards that should be displayed: e.g. picture card, expiration card, nutrition card
#Or more probably the order they should be displayed, e.g. "when does lettuce expire" -> expire card first
def requiredCardTypes(query):
    data={}
    data['object']=query
    data['cards'] = [
        {'name':'Wikipedia_Parse','score':3},
        #{'name':'Other','score':1}
    ]
    return data
