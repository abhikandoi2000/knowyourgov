/**
 * Capitalize first character of each word
 * Eg: "meghe datta" => "Meghe Datta"
 */
var toTitleCase = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

$(function() {
  var fractionComplete = 0.4;
  NProgress.start();
  NProgress.set(fractionComplete);

  // var name = "meghe datta";

  // fetch image from Google Image API (Deprecated)
  // $.ajax({
  //   url: "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + name,
  //   success: function(data, status) {
  //     var imageUrl = data.responseData.results[0].url;
  //     $("#politician-image").attr('src', imageUrl);
  //   }
  // });

  $.ajax({
    url:"/json/politicians/" + name,
    success: function(data, status) {
      $("#info h6.politician-name").html('<a href="/politicians/id/' + data.name + '">' + toTitleCase(data.name) + "</a>");
      $("#personal").append("<div><b>Party: </b>" + toTitleCase(data.party) + "</div>");
      $("#personal").append("<div><b>State: </b>" + toTitleCase(data.state) + "</div>");
      $("#personal").append("<div><b>Constituency: </b>" + toTitleCase(data.constituency) + "</div>");

      fractionComplete += 0.2;
      NProgress.set(fractionComplete);
    }
  });

  $.ajax({
    url: "/json/hindu/" + name,
    success: function(data, status) {

      $("#article-spinner").css('display', 'none');

      for(index in data.articles) {
        article = data.articles[index];
        console.log(article);
        $("#articles").append('<div><b><a href="' + article.url + '">' + article.title + '</a></b><p>' + article.content.substr(0,150) + '...</p></div>');
      }

      fractionComplete += 0.2;
      NProgress.set(fractionComplete);
      NProgress.done();
    }
  });

});