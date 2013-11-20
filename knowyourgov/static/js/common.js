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
    Adds cities in user page
 ***/
function addLocations(locations){


   if(locations.length === 0){
      $('#locations-wrap').html('No past information on your locations from G+. Go add some!')
   }
   for(i in locations){
      $('#locations').append('<a rel="'+ locations[i].value +'" href="#"> ' + locations[i].value + ' </a> , ');
   }
}

$('#locations').delegate('a','click', function(e){

    e.preventDefault();
    $('.results').html('Loading...')

    var city = $(this).text();
    var state = getState(city);

    if(state != 'abroad'){
      $('.results').html('Display Results for ' + state + '');
    }
    else {
      $('.results').html('Only locations within India are supported so far');
    }

})

function signinCallback(authResult) {

  gapi.client.load('plus','v1', function(){

  if (authResult['access_token']) {

    var request = gapi.client.plus.people.get( {'userId' : 'me'} );

    request.execute(function(profile){

      addLocations(profile.placesLived);
      $('#userinfo').html('Welcome, <a href="/user">' + profile.name.givenName +"</a>");

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