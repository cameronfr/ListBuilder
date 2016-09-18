from flask import render_template, request, jsonify
from frontend import app
import cards.queryParser
import cards.card

@app.route('/')
@app.route('/index')
def index():
    return render_template('results.html',
                           title='Home')

@app.route('/ajax/get_cards_html')
def getCardsHtml():
    query = request.args.get('query');
    cardsData = card.generateCards(query);
    cardsHTML = ""
    for card in cardData:
        cardsHTML += render_template('card.html',card=card)
    return cardsHTML
