from flask import render_template, request, jsonify
from frontend import app
from cards import card

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
    for cardData in cardsData:
        cardsHTML += render_template('card.html',card=cardData)
    return cardsHTML
