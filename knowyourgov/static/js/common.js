/***
  A common loader
****/
function showLoading(){
  for( i in arguments ){
    $(arguments[i]).html('<center><img src="/static/img/spinner.gif"></center>')
  }
}

function capitalizeFirstLetter(string){
  return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
  * Fetches News from <Depreciated> Google News API
  * returns {reponseData}
  */
var fetchNews = function(q, callback){
    $.getJSON('https://ajax.googleapis.com/ajax/services/search/news?v=1.0&callback=?&q=' + q, function(res){
      callback(res.responseData);
    })    
}
/**
	* Timeout for ajax calls
	*/
$.ajaxSetup({
	timeout : 30 * 1000
})

$(function(){
  $('.typeahead').typeahead({
    name: 'politicians',
    prefetch: '/json/politicians/all'
  });

});
