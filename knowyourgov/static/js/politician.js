/**
 * Capitalize first character of each word
 * Eg: "meghe datta" => "Meghe Datta"
 */
var toTitleCase = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

/**
  * Flags used to perform sentiment analysis after the last loads
  */
var tweetsLoaded, newsLoaded = false;

/**
  *Performs Sentiment Analysis
  *Variable `analysis_content`
  */
var sentimentAnalysis = function(){

   $('#sentiment-wrap span').css('color','#2980B9');

      if(analysis_content == '') {

        $('#sentiment-wrap .progress').css('display','none');
        $('#sentiment-wrap .palette-paragraph').html('Not enough content is available for Sentiment Analysis');

      } else {

        $.getJSON('https://access.alchemyapi.com/calls/html/HTMLGetRankedNamedEntities?apikey=448588726f2c108b2ddb6a6603d69cd4680361d8&outputMode=json&sentiment=1&jsonp=?&html=' + analysis_content,
          function(response) {

            var entityFound = false;
            for(index in response.entities) {
              rKeywords = response.entities[index].text.toLowerCase().split(" ");
              keywords = name.toLowerCase().split(" ");
              if(rKeywords[rKeywords.length-1] == keywords[keywords.length-1]) {
                // found entity for current politician
                entityFound = true;

                console.log(response.entities[index].sentiment.type);

                $('#sentiment-wrap .palette-paragraph').html(response.entities[index].sentiment.type.toUpperCase());
                if(response.entities[index].sentiment.type == "neutral") {
                  
                  // neutral
                  $('#sentiment-wrap .progress-bar').css('width','50%');

                } else if(response.entities[index].sentiment.type == "positive") {
                  
                  $('#sentiment-wrap .progress-bar').css('width','75%');

                } else if(response.entities[index].sentiment.type == "negative") {
                  
                  $('#sentiment-wrap .progress-bar').css('width','25%');

                } else {
                  
                  $('#sentiment-wrap .progress-bar').css('width','50%');

                }

                // break immediately after entity (politician) is found
                break;
              }
            }

            // entity (politician) not found
            if(!entityFound) {

              $('#sentiment-wrap .progress').css('display','none');
              $('#sentiment-wrap .palette-paragraph').html('Not enough content is available for Sentiment Analysis');

            }

          });

      } // end else

}

showLoading('.tweets');

$(function() {

  /**
   * News Updates For Center Section
   */
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

  /**
   * Fetch news articles from 'The Hindu'
   */
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

  /**
   * Fetch and display tweets (if any)
   */
  $.ajax({
    url: '/json/tweets/search/' + encodeURIComponent(name),
    success: function(data, status) {
      var tweets = data.statuses;
      console.table(tweets);

      // remove spinner
      $('.tweets').html('');

      for(index in tweets) {
        // at max 5 tweets
        if(index == 5) {
          break;
        }

        var tweet = tweets[index];
        var status = tweet.text;
        var screen_name = tweet.user.screen_name;
        var id_str= tweet.id_str;

        $('.tweets').append('<li><a href="https://twitter.com/'+ screen_name +'/status/' + id_str + '" target="_blank"> '+ status +' </a></li>');

        // append tweet for sentiment analysis
        analysis_content += status;
      }

      if(tweets.length == 0) {

        $('.tweets').append('Sorry, no relevant social activity.');
      }
    },
    error: function(xhr, error) {

      tweetsLoaded = true;
      $('.tweets').append('Sorry, unable to fetch tweets.');
    },
    complete: function(xhr, status) {

      tweetsLoaded = true;
      
      if(newsLoaded == true)
        sentimentAnalysis();

    }
  });

});
