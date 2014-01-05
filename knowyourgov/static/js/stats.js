function plotStats(stats)
{
	for(var field in stats)
	{
		var field_stats = stats[field]
		var arr = []
		arr.push([field, 'Number'])
		for(key in field_stats)
			arr.push([toTitleCase(key), field_stats[key]])
		var chart_data = google.visualization.arrayToDataTable(arr);
		var id = field+'_chart'
		var new_div = "<div id='"+id+"' class='chart-div'></div>"
		console.log(new_div)
		$("div#stats").append(new_div)
		drawChart(chart_data, {'title':toTitleCase(field)+' Distribution'}, id)
	}
}

function drawChart(data, options, ele_id) {
    var chart = new google.visualization.PieChart(document.getElementById(ele_id));
    chart.draw(data, options);
}
function toTitleCase(str) {
      str = str.replace('_', ' ')
      return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}