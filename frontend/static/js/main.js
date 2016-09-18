function searchBarSubmitQuery() {
  query = document.getElementById("searchBarCriteria").value;
  $.ajax({
    url: "ajax/get_cards_html",
    data: {
      query: query
    },
    success: addCardHTML,
    error: function(error) {
      console.log(error);
    }
  });
}

var addCardHTML = function(cardHTML, status, qXHR) {
  clearCardHTML();
  document.getElementsByClassName('cardList')[0].insertAdjacentHTML('beforeend', cardHTML);
};
var clearCardHTML = function() {
  var div = document.getElementsByClassName('cardList')[0];
  while (div.firstChild) {
    div.removeChild(div.firstChild);
  }
};
