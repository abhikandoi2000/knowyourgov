$(function(){

	function fadeIn(obj){
		$(obj).fadeIn(1000);
	}
	if(ytube != ""){
		$.getJSON('https://gdata.youtube.com/feeds/api/users/' + ytube +'/uploads?alt=jsonc&max-results=3&v=2', function(d){
			var j = d.data.items;
			for(i in j){
				console.log(j[i].id,j[i].title," - ");
			}
		})
	}
	
})