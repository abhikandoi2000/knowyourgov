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
  $.ajax({
    url: "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + name,
    success: function(data, status) {
      var imageUrl = data.responseData.results[0].url;
      $("#politician-image").attr('src', imageUrl);
    }
  });

  $.ajax({
    url:"/json/politicians/" + name,
    success: function(data, status) {
      $("#info h5.politician-name").html(toTitleCase(data.name));
      $("#personal").append("<div>" + toTitleCase(data.party) + "</div>");
      $("#personal").append("<div>" + toTitleCase(data.state) + "</div>");
      $("#personal").append("<div>" + toTitleCase(data.constituency) + "</div>");

      fractionComplete += 0.2;
      NProgress.set(fractionComplete);
    }
  });

  $.ajax({
    url: "/json/hindu/" + name,
    success: function(data, status) {
      for(index in data.articles) {
        article = data.articles[index];
        console.log(article);
        $("#articles").append('<div><b><a href="' + article.url + '">' + article.title + '</a></b><p>' + article.content.substr(0,150) + '...</p></div>');
      }

      fractionComplete += 0.2;
      NProgress.set(fractionComplete);
    }
  });

  NProgress.done();
});