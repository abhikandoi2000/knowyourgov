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

  // var q = "meghe datta";
  $.ajax({
    url:"/politicians/" + q,
    success: function(data, status) {
      $("#info h6.politician-name").html(toTitleCase(data.name));
      $("#info ul").append("<li>" + toTitleCase(data.party) + "</li>");
      $("#info ul").append("<li>" + toTitleCase(data.state) + "</li>");
      $("#info ul").append("<li>" + toTitleCase(data.constituency) + "</li>");

      fractionComplete += 0.2;
      NProgress.set(fractionComplete);
    }
  });
  // NProgress.done();
});