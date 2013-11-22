/**
 * Capitalize first character of each word
 * Eg: "meghe datta" => "Meghe Datta"
 */
var toTitleCase = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}


showLoading('.tweets');

$(function() {
  // var fractionComplete = 0.4;
  // NProgress.start();
  // NProgress.set(fractionComplete);

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
           analysis_content += status;
        }

        if (tweets.length == 0) {
          $('.tweets').append('Sorry, no relvant social activity.');
        };
        $.getJSON('http://access.alchemyapi.com/calls/html/HTMLGetRankedNamedEntities?apikey=448588726f2c108b2ddb6a6603d69cd4680361d8&outputMode=json&sentiment=1&jsonp=?&html=' + analysis_content,
          function(response) {
            console.log(response);
            for(index in response.entities) {
              if(response.entities[index].text.toLowerCase().substr(0,name.length) == name.substr(0,name.length)) {
                console.log(response.entities[index].sentiment.type);
                $('#sentiment-wrap .palette-paragraph').html(response.entities[index].sentiment.type.toUpperCase());
                if(response.entities[index].sentiment.type == "neutral") {
                  $('#sentiment-wrap .progress-bar').css('width','50%');
                } else if(response.entities[index].sentiment.type == "positive") {
                  $('#sentiment-wrap .progress-bar').css('width','75%');
                } else if(response.entities[index].sentiment.type == "negative") {
                  $('#sentiment-wrap .progress-bar').css('width','25%');
                } else {
                  $('#sentiment-wrap .progress-bar').css('width','50%');
                }
                break;
              }
            }
          });
        // $.ajax({
        //   url: 'http://access.alchemyapi.com/calls/html/HTMLGetRankedNamedEntities?apikey=448588726f2c108b2ddb6a6603d69cd4680361d8&outputMode=json&sentiment=1&html=' + analysis_content,
        //   success: function(data, status) {
        //     console.log(data);
        //   }
        // });
        
    },
    true // this parameter required
  );

  /***
   Filler for Sentiment Analysis
   ***/
   $('#sentiment-wrap span').html('<center> Performing Sentiment Analysis... </center>')

});