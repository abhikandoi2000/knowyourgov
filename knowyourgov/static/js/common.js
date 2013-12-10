/***
  A common loader
****/
function showLoading(e){
  $(e).html('<center><img src="/static/img/spinner.gif"></center>')
}

function capitalizeFirstLetter(string){
  return string.charAt(0).toUpperCase() + string.slice(1);
}

$(function(){
  $('.typeahead').typeahead({
    name: 'politicians',
    prefetch: '/json/politicians/all'
  });

});
