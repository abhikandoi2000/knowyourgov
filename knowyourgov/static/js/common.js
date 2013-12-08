/***
  A common loader
****/
function showLoading(e){
  $(e).html('<center><img src="/static/img/spinner.gif"></center>')
}


$(function(){
  $('.typeahead').typeahead({
    name: 'politicians',
    prefetch: '/json/politicians/all'
  });

});
