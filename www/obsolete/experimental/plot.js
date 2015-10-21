
// generate plot for every ".plot-placeholder" element in the html file
$(function() {
	$(".plot-placeholder").each(
		function(index) {
			var dbtag = $(this).attr("data-dbtag");
			var data = JSON.parse($(this).attr("data-string"));
			var unit = $(this).attr("data-unit");
			var color = $(this).attr("data-linecolor");
			
			//$(this).removeAttr("data-string");
			
// TODO: handle the no data case
			
			// JavaScript uses ms as unit; Python uses s.
			for (var i = 0; i < data.length; i++) {
				data[i][0] = data[i][0]*1000.0;
			}
			
			data = [{ data:data, label:dbtag.concat(" (").concat(unit).concat(")"), color:color }]
			var plot = $.plot($(this), data, 
				   {
						yaxis: {
						   //ticks: [0.01,0.1,1,10,100,1000,10000,100000],
						   //transform:  function(v) { return Math.log(v + 0.000000001); }
						   },
						//xaxis: { mode:"time", timeformat:"%Y/%m/%d %H:%M", minTickSize:[30,"minute"] },
						xaxis: { mode:"time", timeformat:"%Y/%m/%d %H:%M" },
						lines: { show:true },
						points: { show:false },
						selection: { mode:"x" },
						shadowSize: 0
					}
				);
			
			$(this).bind("plotselected", function (event,ranges) {
				alert("From " + ranges.xaxis.from + " to " + ranges.xaxis.to + " (placeholder, not yet implemented)");
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
	);
});
