function searchBarSubmitQuery() {
  criteria = document.getElementById("searchBarCriteria").value;
  contentURL = document.getElementById("searchBarURL").value;
  $.ajax({
    url: "ajax/get_cards_html",
    data: {
      criteria:criteria,
      contentURL:contentURL
    },
    success: addCardHTML,
    error: function(error) {
      console.log(error);
      //have python return error status code -> show error message here
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
