
// generate the html for the plot-container with the plot-placeholder inside (along with the data)
function get_plot(jsonobj) {
	var var_description = jsonobj.description;
	if (var_description.length <= 0) {
		var_description = '';
	}
	var plotplaceholder = $('<div></div>').attr({
		'class':'plot-placeholder',
		'data-tag':jsonobj.tag,
		'data-unit':jsonobj.unit,
		'data-description':var_description,
		'data-linecolor':jsonobj.linecolor,
		'data-points':jsonobj.points
	});
	//plot_this(plotplaceholder);	// won't work on iPhone 4s / iOS6 Safari if this is moved after plotting
	var tmp = $('<div class="plot-container testlayout"></div>')
	.append(plotplaceholder)
	.resizable({
			maxWidth: 1200,
			maxHeight: 800,
			minWidth: 450,
			minHeight: 250
		});
	return tmp;
}

// get a list of pairs of "whatever" values (see the code; for the "at a glance" table)
function get_plot_info(jsonobj) {
	var kv = [];
	var datapoints = JSON.parse(jsonobj.points);
	var bounds = boundaries(datapoints);
	var d = new Date(bounds[1][0]*1000);
	kv.push(['Latest reading',Number((bounds[1][1]).toFixed(2)) + ' ' + jsonobj.unit]);
	kv.push(['Last sampled at',d.toUTCString() + ' (<time class="timeago" datetime="' + d.toISOString() + '">ago</time>)']);
	kv.push(['Time span',get_time_span_string(bounds[1][0] - bounds[0][0])]);
	
	var tmp = [];
	for (var i = 0; i < datapoints.length; i++) {
		tmp.push(datapoints[i][1]);
	}
	kv.push(['Maximum',Number(Math.max.apply(null, tmp).toFixed(2)) + ' ' + jsonobj.unit]);
	kv.push(['Minimium',Number(Math.min.apply(null, tmp).toFixed(2)) + ' ' + jsonobj.unit]);
	
	return kv;
}

// flot (plot) the given plot-placeholder element (it should contain all required data as attributes)
function plot_this(element) {
	var tag = element.attr("data-tag");
	var data = JSON.parse($(element).attr("data-points"));
	var unit = $(element).attr("data-unit");
	var color = $(element).attr("data-linecolor");
	
	//console.log(color);
	
	$(element).removeAttr("data-points");
	
// TODO: handle the no data case

	// x tick labels format depends on the total time span
	var bounds = boundaries(data);
	var oldest = bounds[0][0];
	var latest = bounds[1][0];
	var xsetting = { mode:"time", timeformat:"%Y/%m/%d %H:%M", minTickSize:[15,"minute"] };
	if ((latest - oldest) <= 14*24*3600) {
		xsetting = { mode:"time", timeformat:"%m/%d %H:%M" };
	} else if ((latest - oldest) <= 2*24*3600) {
		xsetting = { mode:"time", timeformat:"%H:%M" };
	}
	
	// JavaScript uses ms as unit; Python uses sec.
	for (var i = 0; i < data.length; i++) {
		data[i][0] = data[i][0]*1000.0;
	}
	
	var labelstr = ' ' + tag;
	if (unit.length > 0) {
		labelstr = labelstr + ' (' + unit + ')';
	}
	//data = [{ data:data, label:tag.concat(" (").concat(unit).concat(")"), color:color }];
	data = [{ data:data, label:labelstr, color:color }];
	var plot = $.plot($(element), data, 
		   {
				yaxis: {},
				//xaxis: { mode:"time", timeformat:"%Y/%m/%d %H:%M", minTickSize:[5,"minute"] },
				xaxis: xsetting,
				lines: { show:true },
				points: { show:false },
				selection: { mode:"x" },
				shadowSize: 0
			}
		);
	
	$(element).bind("plotselected", function(event,ranges) {
		var from = Math.round(ranges.xaxis.from/1000.0);
		var to = Math.round(ranges.xaxis.to/1000.0);
		from = new Date(from*1000);
		to = new Date(to*1000);
		$('#status').html('From ' + from.toUTCString() + ' to ' + to.toUTCString() + ' (zoom not yet implemented)');
	});
	
	// wait til you know AJAX. replace that getData(). TODO
	/*$("#".concat(plot_id)).bind("plotselected", function (event,ranges) {
alert("You selected " + ranges.xaxis.from + " to " + ranges.xaxis.to);
		
		if (ranges.xaxis.to - ranges.xaxis.from < 0.00001) {
			ranges.xaxis.to = ranges.xaxis.from + 0.00001;
		}
		if (ranges.yaxis.to - ranges.yaxis.from < 0.00001) {
			ranges.yaxis.to = ranges.yaxis.from + 0.00001;
		}
		
		plot = $.plot("#".concat(plot_id), getData(ranges.xaxis.from, ranges.xaxis.to),
			$.extend(true, {}, options, {
				xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
				yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
			})
		);
		
		plot.setSelection(ranges);
	});*/
}

// find all plot-placeholder elements and reder the plots in them
function plot_all() {
	$(".plot-placeholder").each(
		function(index,element) {
			plot_this($(element));
		}
	);
}

// generate plot for every ".plot-placeholder" element in the html file
//$(plot_all); is really $(document).ready(plot_all);
