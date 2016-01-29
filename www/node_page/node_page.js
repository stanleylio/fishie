(function() {
	var site = $("#data-id").data("site");
	var node_id = $("#data-id").data("node_id");

	$.get("../node_config.py?p=node_name&site=" + site + "&node_id=" + node_id,function(data) {
		$("#node_name").html(data.node_name);
		document.title = site + " | " + data.node_name + " (" + node_id + ")";
	});

	$("#node_id").append(node_id);
	
	$.get("../node_config.py?p=node_note&site=" + site + "&node_id=" + node_id,function(data) {
		$("#node_note").html(data.node_note);
	});

	//http://stackoverflow.com/questions/25876274/jquery-data-not-working
	//".data() doesn't set data-* attributes."
	var d = new Date(Date.now());
	tmp = $('<time class="timeago"></time>').attr('datetime',d.toISOString()).html('ago');
	$('<p></p>').append(tmp.prop('outerHTML')).appendTo('#pagegeneratedts');

	$.get("../node_config.py?p=latest_sample&site=" + site + "&node_id=" + node_id,function(data) {
		//console.log(data.latest_sample);
		var d;
		if ('ReceptionTime' in data.latest_sample) {
			d = new Date(data.latest_sample['ReceptionTime']*1000);
		} else if ('Timestamp' in data.latest_sample) {
			d = new Date(data.latest_sample['Timestamp']*1000);
		}
		var tmp = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
		$('<p></p>').append(tmp.prop('outerHTML')).appendTo('#lastsampledts');
		$("time.timeago").timeago();
	});

	$.get("../node_config.py?p=latest_sample&p=units&site=" + site + "&node_id=" + node_id,function(data) {
		$("#latest_table").append("<tr><th>Variable</th><th>Value</th><th>Unit</th></tr>");
		
		/*$.each(data['latest_sample'],function(tag){
			$("#latest_table").append("<tr><td><a href=\"#\" title=\"click for self-updating plot\" target=\"_blank\">" + tag + "</a></td><td>" + data.latest_sample[tag] + "</td><td>" + data.units[tag] + "</td></tr>");
		});*/

		$.get("../node_config.py?p=list_of_disp_vars&site=" + site + "&node_id=" + node_id,function(tmp) {
			$.each(tmp.list_of_disp_vars,function(i,tag) {
				//console.log(tag);
				//var tgt = "../" + site + "/" + node_id + "/" + tag + ".png";
				
				var tgt = "../experimental3/?site=" + site + "&node_id=" + node_id + "&variable=" + tag;
				
				$("#latest_table").append("<tr><td><a href=\"" + tgt + "\" title=\"click for self-updating plot\">" + tag + "</a></td><td>" + data.latest_sample[tag] + "</td><td>" + data.units[tag] + "</td></tr>");
			});
		});
	});

	$.get("../node_config.py?p=list_of_disp_vars&p=description&site=" + site + "&node_id=" + node_id,function(data) {
		var desc_map = data.description;
		$.each(data.list_of_disp_vars,function(i,v) {

			var img_src = "../" + site + "/" + node_id + "/" + v + ".png";
			var img_prop = "../" + site + "/" + node_id + "/" + v + ".json";
			
			// generate the caption (plot generation time, plot time span etc.)
			$.get(img_prop,function(data) {
				var d = new Date(data['plot_generated_at']*1000);
				var ts_plot = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
				d = new Date(data['time_end']*1000);
				var ts_sample = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
				
				var span = data['time_end'] - data['time_begin'];
				var nday = Math.floor(span/24/60/60);
				var remain = span % (24*60*60);
				var nhour = Math.floor(span/60/60);
				span = Math.floor(remain/3600) + " hours";
				if (nday > 0) {
					span = nday + " days, " + span;
				}


				var caption = $('<div class="caption"></div>')
				//.append("<h4>" + v + "</h4>")
				.append("<h4>" + desc_map[v] + "</h4>")
				//.append("<p>" + 'Latest sample at ' + ts_sample.prop('outerHTML') + "</p>")
				.append("<p>" + 'Plot generated ' + ts_plot.prop('outerHTML') + "</p>")
				.append('<p>' + data["data_point_count"] + " samples | " + span + '</p>');

				var tmp = $('<div class="col-xs-12 col-sm-6 col-lg-4" sortby="' + v + '"></div>');
				$('<a class="thumbnail" href="' + img_src + '"></a>')
				.append('<img class="img-responsive" src="' + img_src + '">')
				.append(caption)
				.appendTo(tmp);
				
				$("#static_plots").append(tmp);
				
				$("time.timeago").timeago();
			});
		});
	});
})();