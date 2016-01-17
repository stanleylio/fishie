(function() {
	var site = $("#data-id").data("site");
	var node_id = $("#data-id").data("node_id");
	var variable = $("#data-id").data("variable");;
	// TODO
	var end = Date.now()/1000.0;
	var begin = end - 1*24*60*60;
	
	// query for sensor data
	$.get("../qtr.py?site=poh&node_id=" + node_id + "&var=" + variable + "&begin=" + begin + "&end=" + end,function(data) {
		var ts = data.qtr['Timestamp'];
		if ('ReceptionTime' in data.qtr) {
			ts = data.qtr['ReceptionTime'];
		}
		var r = data.qtr[variable];
		
		var layout = {
		  title: site + ' | ' + node_id + ' | ' + variable,
		  titlefont: {
			  family: 'Helvetica, monospace',
		  },
		  autosize: false,
		  width: 960,
		  height: 500,
		  xaxis: {
			title: 'Time',
			titlefont: {
			  family: 'Helvetica, monospace',
			  size: 18,
			  color: '#7f7f7f'
			}
		  },
		  yaxis: {
			title: 'too much trouble to add unit',
			titlefont: {
			  family: 'Helvetica, monospace',
			  size: 18,
			  color: '#7f7f7f'
			}
		  },
		  margin: { l:50, r:50, b:50, t:50, pad:4 }
		};
		
		Plotly.plot( $('#tester')[0],
					[{ x: ts, y: r, name: variable, mode: "markers"}],
					layout
					);
	});
})();