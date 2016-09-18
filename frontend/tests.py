from flask import Flask
from flask.ext.testing import TestCase
from cards import queryParser
import unittest
import json

class web_tests(TestCase):

    def create_app(self):
        app = Flask('search')
        app.config['TESTING'] = True
        return app

    def test_query_required_cards(self):
        q = "tomato"
        requiredCards = query.requiredCardTypes(q)
        self.assertEqual(requiredCards['object'],"tomato");

class ajax_tests(TestCase):

    def create_app(self):
        app = Flask('search')
        app.config['TESTING'] = True
        return app

class search_tests(TestCase):

    def create_app(self):
        app = Flask('search')
        app.config['TESTING'] = True
        return app

class learning_tests(TestCase):

    def create_app(self):
        app = Flask('search')
        app.config['TESTING'] = True
        return app
