from flask import render_template, request, jsonify
from search import app
from cards import query as Query
from cards import card as Card



@app.route('/')
@app.route('/index')
def index():
    return render_template('results.html',
                           title='Home')

#ajax and non ajax version
#ajax versions shows cards one at a time
#non ajax version shows all cards, i.e. render_template('results.html')
@app.route('/ajax/get_required_cards')
def getRequiredCards():
    query = request.args.get('query');
    cards = jsonify(Query.requiredCardTypes(query))
    return cards

@app.route('/ajax/get_card_html')
def getCardHtml():
    object = request.args.get('object');
    cardType = request.args.get('card');
    cardData = Card.generateCard(object,cardType);

    cardsHTML = ""
    for card in cardData:
        cardsHTML += render_template('card.html',card=card)
    return cardsHTML
