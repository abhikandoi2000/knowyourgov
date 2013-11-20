function signinCallback(authResult) {

  gapi.client.load('plus','v1', function(){

  if (authResult['access_token']) {

    var request = gapi.client.plus.people.get( {'userId' : 'me'} );

    request.execute(function(profile){

      console.log(profile.name.givenName, profile.placesLived);

      $('#userinfo').html('Welcome, <a href="/user">' + profile.name.givenName +"</a>");

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