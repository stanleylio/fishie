(function() {
	var site = $("#data-id").data("site");
	var node_id = $("#data-id").data("node_id");
	var variable = $("#data-id").data("variable");;
	// TODO
	var end = Date.now()/1000.0;
	var begin = end - 7*24*60*60;
	
	// query for sensor data
	$.get("../qtr.py?site=" + site + "&node_id=" + node_id + "&var=" + variable + "&begin=" + begin + "&end=" + end,function(data) {
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
			title: new Date().toString().split(/(\(.*\))/)[1],
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
		
		var offset = (new Date).getTimezoneOffset()*60;
		for (var i = 0; i < ts.length; i++) {
			//ts[i] = (new Date(ts[i]*1000)).toISOString().replace('T',' ').replace('Z','');
			ts[i] = (new Date((ts[i] - offset)*1000)).toISOString().replace('T',' ').replace('Z','');
		}

		Plotly.plot( $('#tester')[0],
					[{ x: ts, y: r, name: variable, mode: "markers"}],
					layout
					);
	});
})();