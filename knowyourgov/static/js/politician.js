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
    url:"/json/politicians/" + name,
    success: function(data, status) {
      $("#info h6.politician-name").html(toTitleCase(data.name));
      $("#info ul").append("<li>" + toTitleCase(data.party) + "</li>");
      $("#info ul").append("<li>" + toTitleCase(data.state) + "</li>");
      $("#info ul").append("<li>" + toTitleCase(data.constituency) + "</li>");

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
  // NProgress.done();
});