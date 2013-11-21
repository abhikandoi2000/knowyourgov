/***

    getState -
    Given a city, uses Geocode API to return state and check for country

****/
var getState = function(city){

  var state, country;

  $.ajax({
      url :'http://maps.googleapis.com/maps/api/geocode/json?address='+ city +'&sensor=true',
      async : false
  }).done(function(response){
    // 1 - locality, 2 - Admin[2], 3 - Admin[1], 4 - Country
    var res = response['results'][0]['address_components'];
        console.log(response)
        console.log(res)
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
  //ToDo - format & display
  console.log(state);
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

   if(locations.length === 0){
      $('#gplusinfo').append('<br><small>No past information on your locations from G+. Go add some!</small>')
   }
   $('#gplusinfo').append('<br>We see you have lived in ')
   for(i in locations){
      $('#gplusinfo').append('<a rel="'+ locations[i].value +'" href="#"> ' + locations[i].value + ' </a> , ');
   }
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


var geolocation = function(){

  if(navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        // map.setCenter(initialLocation);
          console.log(lat,lng)

         $.get('http://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+lng+'&sensor=false', function(response){
            var state = response['results'][response['results'].length - 2]['address_components'][0].long_name;
            searchState(state);
            $('#geo').html('<small>Current Location : ' +  response['results'][0]['formatted_address'] + '</small>');
          })
      
      },

        function(error){
          console.log(error)
        },

        {timeout : 10000}
      )

  }
  else {
    
  }

}

if(!navigator.geolocation){
  $('#btn-detect').prop('disabled', true).addClass('disabled');
  $('.geo-info').html('<small>Your Browser doesn\'t support browser location')
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

/***
  Callback for G+ Sign-In
 ***/
function signinCallback(authResult) {

  gapi.client.load('plus','v1', function(){

  if (authResult['access_token']) {

    var request = gapi.client.plus.people.get( {'userId' : 'me'} );

    request.execute(function(profile){
      $('#gplusinfo').html('Welcome, ' + profile.name.givenName + ".");
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