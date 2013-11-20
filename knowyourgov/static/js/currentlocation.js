if(navigator.geolocation) {

  console.log('1')

  navigator.geolocation.getCurrentPosition(function(position) {
      var lat = position.coords.latitude,
          lng = position.coords.longitude;
      // map.setCenter(initialLocation);
        console.log(lat,lng)

       // $.get('http://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+lng+'&sensor=false', function(response){
       //    console.log(response);
       //    $('#map-canvas').html('Current Location : ' +  response['results'][0]['formatted_address']);
       //  })
    
    },

      function(error){
        console.log(error)
      },

      {timeout : 10000}
    )

}
else {

  console.log('False')
}