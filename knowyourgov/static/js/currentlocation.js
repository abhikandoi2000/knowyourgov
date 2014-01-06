/**
 * Capitalize first character of each word
 * Eg: "meghe datta" => "Meghe Datta"
 */
var toTitleCase = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

/***

    getState -
    Given a city, uses Geocode API to return state and check for country

****/
var getState = function(city){

  var state, country;

  $.ajax({
      url :'https://maps.googleapis.com/maps/api/geocode/json?address='+ city +'&sensor=true',
      async : false
  }).done(function(response){
    // 1 - locality, 2 - Admin[2], 3 - Admin[1], 4 - Country
    var res = response['results'][0]['address_components'];
        // console.log(response)
        // console.log(res)
        state = res[res.length - 2].long_name;
        country = res[res.length - 1].long_name;

  })

  if(country !== 'India')
    return 'abroad';
  else
    return state;

}
/***
    Given a state populate results in tabular form 
***/
var searchState = function(state){
    showLoading('.results');

  $.ajax({
    
    url: '/json/politicians/state/' + state.toLowerCase(),

    success: function(data, success) {  

      $('#res-title').show();
      var table = $('<table class="table table-hover"></table>');
      var tbody = $('<tbody></tbody>');
      var head_row = $('<tr><th>Name</th><th>Party</th><th>Constituency</th><th>State</th></tr>');

      tbody.append(head_row);
      // populate the table
      for(index in data.politicians) {
        politician = data.politicians[index];

        tbody.append('<tr><td><a href="/politicians/id/' + politician.name.replace(/ /g,'-') + '">' + toTitleCase(politician.name) + '</a></td><td><a href="/party/'+ politician.party+'">' + toTitleCase(politician.party) + '</a></td><td>' + (politician.constituency == '' ? '-' : toTitleCase(politician.constituency) ) + '</td><td><a href="/state/'+politician.state+'">' + toTitleCase(politician.state) + '</a></td></tr>');
      }

      table.append(tbody);

      // clear the results
      $('.results').html('');
      // append the table
      if(data.politicians.length == 0)
        $('.results').append('<center> Sorry, no results found!. Our database is of Indian politicians only. <p> <small> Are we missing on anyone important? <a href="/about#feedback"> Report it </a> </small></p></center>');
      else
        $('.results').append(table);
    
    }
  });
  // console.log(state);
}
/***
  Used for Custom Search
****/
var searchbyLocation = function(){
  var l = $('#l').val(),
      state = getState(l);
      searchState(state);
}
/***
    Adds cities after G+ Sign  - In
 ***/
function addLocations(locations){

   $('#gplusinfo').append('<br>We see you have lived in ')
   for(i in locations){
      $('#gplusinfo').append('<a rel="'+ locations[i].value +'" href="#"> ' + capitalizeFirstLetter(locations[i].value) + ' </a>');
      if(i == locations.length - 1)
        break;
      $('#gplusinfo').append(', ');
   }
   $('#gplusinfo').append('<p class="palette-paragraph">Click on the region whose search you want</p> ')
}
/***
  Callback for G+ Sign-In
 ***/
function signinCallback(authResult) {

  gapi.client.load('plus','v1', function(){

  if (authResult['access_token']) {

    var request = gapi.client.plus.people.get( {'userId' : 'me'} );

    request.execute(function(profile){
      $('#gplusinfo').html('Welcome, ' + profile.name.givenName + ".");

      if(typeof profile.placesLived == "undefined")
        $('#gplusinfo').append('<br><small>No past information on your locations from G+. Go add some!</small>');
      else
       addLocations(profile.placesLived);

    });

    // Update the app to reflect a signed in user
    // Hide the sign-in button now that the user is authorized, for example:
    document.getElementById('signinButton').setAttribute('style', 'display: none');

    $('.notloggedin').hide();
    $('.loggedin').show();

    } else if (authResult['error']) {
      // Update the app to reflect a signed out user
      // Possible error values:
      //   "user_signed_out" - User is signed-out
      //   "access_denied" - User denied access to your app
      //   "immediate_failed" - Could not automatically log in the user
      // console.log('Sign-in state: ' + authResult['error']);
    }

  });

}
/***
  Handler for clicks on cities imported from G+
 ***/
$('#gplusinfo').delegate('a','click', function(e){

    e.preventDefault();

    var city = $(this).text();
    var state = getState(city);

    searchState(state);

})

var plotOnMap = function(lat,lng){
    var mapOptions = {
          center: new google.maps.LatLng(lat,lng),
          zoom: 10
    };
       
     var map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);
}

var geolocation = function(){

  if(navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        // map.setCenter(initialLocation);
          plotOnMap(lat,lng)

         $.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+lng+'&sensor=false', function(response){
            var state = response['results'][response['results'].length - 2]['address_components'][0].long_name;
            searchState(state);
            $('#geo').removeClass('center').html('<small>Current Location : ' +  response['results'][0]['formatted_address'] + '</small>');
          })
      
      },

        function(error){
          $('#geo').html('<small>Your location cannot be mapped precisely, please try other methods</small>')
        },

        {timeout : 10000}
      )

  }
  else {
    
  }

}

if(!navigator.geolocation){
  $('#btn-detect').prop('disabled', true).addClass('disabled');
  $('#map-canvas').html('<small>Your Browser doesn\'t support browser location')
}

$('#btn-detect').on('click', function(){
  geolocation();
  $('#btn-detect').hide();
  showLoading('#geo')
})

$('#l-form').on('submit', function(e){
  e.preventDefault();
})

$('#l').on('keyup', function(e){
    if( e.keyCode == 13 )
      searchbyLocation();
})
$('#l-search').on('click', searchbyLocation)

