/**
 * Capitalize first character of each word
 * Eg: "meghe datta" => "Meghe Datta"
 */
var toTitleCase = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}


showLoading('.tweets');

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

  /***
    News Updates For Center Section
   ***/

    // google.load('search',1);  

    // function onGLoad(){
        
    //   newsSearch = new google.search.NewsSearch();
    //   newsSearch.setSearchCompleteCallback(this, searchComplete, null);

    //   newsSearch.execute(name);
    // }

    // google.setOnLoadCallback(onGLoad);

   // $.ajax({
   //    url :'https://news.google.com/news/feeds?q=' +name+'&output=rss',
   //    dataType : "xml"

   // }).done(function(xml){
   //    var html  = '';
   //    console.log($(xml))
   //    var e = $(xml).find('item').filter('first');
   //    html += '<div><a href="' + e.find('link').text() + '" target="_blank"> ' + e.find('title').text() +'</a></div>';
   //    html += '<div> ' + e.find('description').text()+ ' </div>';

   //    $('#news-wrap').html(html);

   // })

  $.ajax({
    url:"/json/politicians/" + name,
    success: function(data, status) {
      var special = '';
      if( data.state == '' && data.constituency == '' ) {
        special = 'Cabinet Minister';
      } else if( data.constituency == '' ) {
        special = 'CM of ' + toTitleCase(data.state);
      } else {
        special = '';
      }
      $("#politician-image").css('background-image', "url('" + data.imageUrl + "')");
      $("#info h6.politician-name").html('<a href="/politicians/id/' + data.name + '">' + toTitleCase(data.name) + "</a>");
      $("#personal").append("<div><i>" + special + "</i></div>");
      $("#personal").append("<div><b>Party       </b><br>" + toTitleCase(data.party) + "</div>");
      $("#personal").append("<div><b>State       </b><br>" + ( data.state == '' ? '-' : toTitleCase(data.state) ) + "</div>");
      $("#personal").append("<div><b>Constituency</b><br>" + ( data.constituency == '' ? '-' : toTitleCase(data.constituency) ) + "</div>");

      fractionComplete += 0.2;
      NProgress.set(fractionComplete);
    }
  });

  // $.ajax({
  //   url: "/json/hindu/" + name,
  //   success: function(data, status) {

  //     $("#article-spinner").css('display', 'none');

  //     for(index in data.articles) {
  //       article = data.articles[index];
  //       console.log(article);
  //       $("#articles").append('<div><b><a href="' + article.url + '">' + article.title + '</a></b><p>' + article.content.substr(0,150) + '...</p></div>');
  //     }

  //     fractionComplete += 0.2;
  //     NProgress.set(fractionComplete);
  //     NProgress.done();
  //   }
  // });

  cb.__call(
    "search_tweets",
    "q="+ name,
    function (reply) {

        $('.tweets').html('');

        var tweets = reply['statuses'];

        console.log(tweets);

        for(var i = 0; i < 5; i++){
          var status = tweets[i].text;
           $('.tweets').append('<li><a href="https://twitter.com/'+ tweets[i].user.screen_name +'/status/'+tweets[i].id_str+'" target="_blank"> '+ status +' </a></li>');
        }

        
    },
    true // this parameter required
  );

  /***
   Filler for Sentiment Analysis
   ***/
   $('#sentiment-wrap span').html('<center> Performing Sentiment Analysis... </center>')

});