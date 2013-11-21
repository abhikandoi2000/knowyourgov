var searchState = function(state){
  console.log(state);
}

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