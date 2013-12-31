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

var formatNews = function(responseData){
  
  $('#news-wrap').html('');

  var html = '';
  var res = responseData.results;

  // res.replace(/(<([^>]+)>)/ig,"");

  if(res.length > 0){
    // first news article
    html += '<div><div class="news-title"><a href="'+ decodeURIComponent(res[0].url) +'" target="_blank">';
    html += res[0].title.replace(/(<([^>]+)>)/ig,"") + '</a></div><div class="news-desc">';

    // load image, only if present
    html += (typeof res[0].image == "undefined" ? '' : '<div class="pull-right"><img src="'+res[0].image.tbUrl.replace(/^http:\/\//i, 'https://')+'"></div>');

    html += res[0].content.replace(/(<([^>]+)>)/ig,"") + '</div></div>';

    // update content for sentiment analysis
    analysis_content.push(res[0].title.replace(/(<([^>]+)>)/ig,""));
    analysis_content.push(res[0].content.replace(/(<([^>]+)>)/ig,""));

    // second news article if it exists
    if(res.length > 1) {
      html += '<div><div class="news-title"><a href="'+ decodeURIComponent(res[1].url) +'" target="_blank">';
      html += res[1].title.replace(/(<([^>]+)>)/ig,"") +'</a></div><div class="news-desc">';

     // load image, only if present
      html += (typeof res[1].image == "undefined" ? '' : '<div class="pull-right"><img src="'+res[1].image.tbUrl.replace(/^http:\/\//i, 'https://')+'"></div>');

      html += res[1].content.replace(/(<([^>]+)>)/ig,"") + '</div></div>';

     // update content for sentiment analysis
    analysis_content.push(res[1].title.replace(/(<([^>]+)>)/ig,""));
    analysis_content.push(res[1].content.replace(/(<([^>]+)>)/ig,""));

    }

    // archive(other) articles
    for(var i = 2; i < res.length; ++i){

      if(i != 0 && i != 1) {

        html += '<div class="news-title"><a href="'+ decodeURIComponent(res[i].url) +'" target="_blank">'+ res[i].title.replace(/(<([^>]+)>)/ig,"") +'</a></div>';

        // update content for sentiment analysis
        analysis_content.push(res[i].title.replace(/(<([^>]+)>)/ig,""));
      }

    }

    // update news section
    $('#news-wrap').html(html);

  } else {

    // no relevant news articles
    var html = '<div style="text-align:center;">Sorry, no relevant articles.';

    html += '</div>';

    // update news section
    $('#news-wrap').html(html);
    
  } // end else

  newsLoaded = true;
  
  if(tweetsLoaded == true)
    sentimentAnalysis();

}

/**
  *Performs Sentiment Analysis
  *Variable `analysis_content`
  */
var sentimentAnalysis = function(){

   $('#sentiment-wrap span').css('color','#2980B9');

      analysis_content_string = analysis_content.join(' ');
      
      console.log(analysis_content, analysis_content_string);
      if(analysis_content_string == '') {

        $('#sentiment-wrap .progress').css('display','none');
        $('#sentiment-wrap .palette-paragraph').html('Not enough content is available for Sentiment Analysis');

      } else {

        $.getJSON('https://access.alchemyapi.com/calls/html/HTMLGetRankedNamedEntities?apikey=448588726f2c108b2ddb6a6603d69cd4680361d8&outputMode=json&sentiment=1&jsonp=?&html=' + analysis_content_string,
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

var plotAttendance = function(percent){
  var ctx = document.getElementById("attendanceChart").getContext("2d");

  var data = [
    { value: percent, color : '#F39C12' },
    { value: 100 - percent, color : '#ECF0F1'}
  ]

  var options = {};

  var attendanceChart = new Chart(ctx).Doughnut(data, options);


}

$(function() {


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

  fetchNews(name, formatNews)

  /**
    * Checks whether attendance is available
    */
    if($('canvas#attendanceChart').length > 0){

      var attendance = parseInt($('canvas#attendanceChart').data('attendance'));
      
      if(typeof attendance == "number" && attendance != 0){
        plotAttendance(attendance);
      }
    }

  /**
   * Fetch and display tweets (if any)
   */
  $.ajax({
    url: '/json/tweets/search/' + encodeURIComponent(name),
    success: function(data, status) {
      var tweets = data.statuses;
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
        analysis_content.push(status);

      }

      if(tweets.length == 0) {

        $('.tweets').append('Sorry, no relevant social activity.');
      }
    },
    error: function(xhr, error) {

      tweetsLoaded = true;
      $('.tweets').html('');
      $('.tweets').append('Sorry, unable to fetch tweets.');
    },
    complete: function(xhr, status) {

      tweetsLoaded = true;
      
      if(newsLoaded == true)
        sentimentAnalysis();

    }
  });

});
