/**
 * Capitalize first character of each word
 * Eg: "meghe datta" => "Meghe Datta"
 */
var toTitleCase = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
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
   * Fetch and update information about politician
   * includes image, name, party, state and constituency
   */
  $.ajax({
    url:"/json/politicians/" + name,
    success: function(data, status) {

      var special = '';
      if( data.state == '' && data.constituency == '' ) {

        special = 'Cabinet Minister';

      } else if( data.constituency == '' ) {

        special = 'CM of ' + toTitleCase(data.state);

      }

      // update image and other personal information for politician
      $("#politician-image").css('background-image', "url('" + data.imageUrl + "')");

      $("#info h6.politician-name").html('<a href="/politicians/id/' + data.name + '">' + toTitleCase(data.name) + "</a>");

      $("#personal").append("<div><i>" + special + "</i></div>");
      $("#personal").append("<div><b>Party       </b><br>" + toTitleCase(data.party) + "</div>");
      $("#personal").append("<div><b>State       </b><br>" + ( data.state == '' ? '-' : toTitleCase(data.state) ) + "</div>");
      $("#personal").append("<div><b>Constituency</b><br>" + ( data.constituency == '' ? '-' : toTitleCase(data.constituency) ) + "</div>");

    } // end success
  });

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
  cb.__call(
    "search_tweets",
    "q="+ name,
    function (reply) {

      // empty tweets section (just in case)
      $('.tweets').html('');

      var tweets = reply['statuses'];

      // console.log('tweets');
      // console.log(tweets);

      if(typeof tweets == "undefined" || tweets.length == 0){
        $('.tweets').append('<small>Sorry, no relevant social activity.</small>');
      }
      else {
        for(var i = 0; i < Math.min(5, tweets.length); i++){
          try {
            var status = tweets[i].text;
            $('.tweets').append('<li><a href="https://twitter.com/'+ tweets[i].user.screen_name +'/status/'+tweets[i].id_str+'" target="_blank"> '+ status +' </a></li>');

             // append tweet for sentiment analysis
             analysis_content += status;

            if (tweets.length == 0) {
              $('.tweets').append('Sorry, no relevant social activity.');
            }
          } catch(e) {
            // console.log('Problem with tweet:');
            // console.log(tweets[i]);
          }
        }
      }

      $('#sentiment-wrap span').css('color','#2980B9');
      // console.log('Request Sent');

      if(analysis_content == '') {

        $('#sentiment-wrap .progress').css('display','none');
        $('#sentiment-wrap .palette-paragraph').html('Not enough content is available for Sentiment Analysis');

      } else {
        $.getJSON('https://access.alchemyapi.com/calls/html/HTMLGetRankedNamedEntities?apikey=448588726f2c108b2ddb6a6603d69cd4680361d8&outputMode=json&sentiment=1&jsonp=?&html=' + analysis_content,
          function(response) {
            console.log(response);
            var entityFound = false;
            for(index in response.entities) {
              if(response.entities[index].text.toLowerCase().substr(0,name.length) == name.substr(0,name.length)) {
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
    },
    true // this parameter required
  );

});