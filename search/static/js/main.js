function searchBarSubmitQuery() {
  query = document.getElementById("searchBarCriteria").value;
  $.ajax({
    url: "ajax/get_required_cards",
    data: {
      query: query
    },
    success: processCardList,
    error: function(error) {
      console.log(error);
    }
  });
}

var processCardList = function(cardList, statusj, qXHR) {
  console.log("Recieved card list:" + cardList);
  clearCardHTML()
  cardListParsed = cardList; //JSON.parse(cardList);
  cards = cardListParsed.cards;
  object = cardListParsed.object;
  for (var i = 0; i < cards.length; i++) {
    $.ajax({
      url: "ajax/get_card_html",
      data: {
        object: object,
        card: cards[i].name
      },
      success: addCardHTML,
      error: function(error) {
        console.log(error);
      }
    });
  }
};

var addCardHTML = function(cardHTML, status, qXHR) {
  //console.log(cardHTML);
  document.getElementsByClassName('cardList')[0].insertAdjacentHTML('beforeend', cardHTML);
};
var clearCardHTML = function() {
  var div = document.getElementsByClassName('cardList')[0];
  while (div.firstChild) {
    div.removeChild(div.firstChild);
  }
};
