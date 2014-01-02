var formatNews = function(responseData){
  
  $('.news-wrap').html('');

  var html = '';
  var res = responseData.results;


  if(res.length > 0){
    // first news article
    html += '<div><div class="news-title"><a href="'+ decodeURIComponent(res[0].url) +'" target="_blank">';
    html += res[0].title.replace(/(<([^>]+)>)/ig,"") + '</a></div><div class="news-desc">';

    // load image, only if present
    html += (typeof res[0].image == "undefined" ? '' : '<div class="pull-right"><img src="'+res[0].image.tbUrl.replace(/^http:\/\//i, 'https://')+'"></div>');

    html += res[0].content.replace(/(<([^>]+)>)/ig,"") + '</div></div>';


    // second news article if it exists
    if(res.length > 1) {
      html += '<div><div class="news-title"><a href="'+ decodeURIComponent(res[1].url) +'" target="_blank">';
      html += res[1].title.replace(/(<([^>]+)>)/ig,"") +'</a></div><div class="news-desc">';

     // load image, only if present
      html += (typeof res[1].image == "undefined" ? '' : '<div class="pull-right"><img src="'+res[1].image.tbUrl.replace(/^http:\/\//i, 'https://')+'"></div>');

      html += res[1].content.replace(/(<([^>]+)>)/ig,"") + '</div></div>';

    }

    // archive(other) articles
    for(var i = 2; i < res.length; ++i){

      if(i != 0 && i != 1) {

        html += '<div class="news-title"><a href="'+ decodeURIComponent(res[i].url) +'" target="_blank">'+ res[i].title.replace(/(<([^>]+)>)/ig,"") +'</a></div>';

      }

    }

    // update news section
    $('.news-wrap').html(html);

  } else {

    // no relevant news articles
    var html = '<div style="text-align:center;">Sorry, no relevant articles.';

    html += '</div>';

    // update news section
    $('.news-wrap').html(html);
    
  } // end else

}

$(function(){

	if(ytube != ""){
		$.getJSON('https://gdata.youtube.com/feeds/api/users/' + ytube +'/uploads?alt=jsonc&max-results=2&v=2', function(d){
			var j = d.data.items;
			h = '';
			$('.video-wrap').html('');
			for(i in j){
				h += '<p class="palette-paragraph">' + j[i].title +' </p><iframe id="ytplayer" type="text/html" src="http://www.youtube.com/embed/'+ j[i].id +'?autoplay=0&autohide=1&controls=0&showinfo=0&theme=light" frameborder="0"/>';			
			}
			$('.video-wrap').html(h)
		})
	}
	
	fetchNews(title, formatNews)

})