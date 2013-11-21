// // AIzaSyCt302Eg6wtngduThQ9jEmcGQfHmn1XNQg

// var initialLocation;
// var siberia = new google.maps.LatLng(60, 105);
// var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);
// var browserSupportFlag =  new Boolean();

// function initialize() {
//   var mapOptions = {
//     zoom: 8,
//     center: new google.maps.LatLng(-34.397, 150.644),
//     mapTypeId: google.maps.MapTypeId.ROADMAP
//     // region: 'IN'
//   };

//   var map = new google.maps.Map(document.getElementById('map-canvas'),
//       mapOptions);

//   // Try W3C Geolocation (Preferred)
//   if(navigator.geolocation) {
//     browserSupportFlag = true;
//     navigator.geolocation.getCurrentPosition(function(position) {
//       initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
//       map.setCenter(initialLocation);
//     }, function() {
//       handleNoGeolocation(browserSupportFlag);
//     });
//   }
//   // Browser doesn't support Geolocation
//   else {
//     browserSupportFlag = false;
//     handleNoGeolocation(browserSupportFlag);
//   }

//   function handleNoGeolocation(errorFlag) {
//     if (errorFlag == true) {
//       alert("Geolocation service failed.");
//       initialLocation = newyork;
//     } else {
//       alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
//       initialLocation = siberia;
//     }
//     map.setCenter(initialLocation);
//   }
	
// }

// // google.maps.visualRefresh = true;

// // function loadScript() {
// //   var script = document.createElement('script');
// //   script.type = 'text/javascript';
// //   script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=true&' +
// //       'callback=initialize';
// //   document.body.appendChild(script);
// // }

// window.onload = initialize;
  
if(navigator.geolocation) {
  $('#geoloc-success').show();
}

var googleapi = {

  signin : function(authResult){

     gapi.client.load('plus','v1', function(){
       googleapi.locations();
     });

  },

  locations : function(){}

}

function signinCallback(authResult) {

  gapi.client.load('plus','v1', function(){

  if (authResult['access_token']) {

    var request = gapi.client.plus.people.get( {'userId' : 'me'} );

    request.execute(function(profile){
      console.log(profile.name.givenName, profile.placesLived)
    });

    // Update the app to reflect a signed in user
    // Hide the sign-in button now that the user is authorized, for example:
    document.getElementById('signinButton').setAttribute('style', 'display: none');

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
    // var msg = "Your browser supports location detection, Sweet!"
    // browserSupportFlag = true;
    // navigator.geolocation.getCurrentPosition(function(position) {
    //   var lat = position.coords.latitude,
    //       lng = position.coords.longitude;
    //   // map.setCenter(initialLocation);

    //    $.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+lng+'&sensor=false', function(response){
    //       console.log(response);
    //       $('#map-canvas').html('Current Location : ' +  response['results'][0]['formatted_address']);
    //     })
    // }, function() {
        


    // });



