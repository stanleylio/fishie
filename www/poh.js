
/*$.get("node_config.py?p=node_name",function(data) {
	$("#node_name").html(data.node_name);
	document.title = data.node_name;
});*/

/*$.get("node_config.py?p=node_note",function(data) {
	$("#node_note").append(data.node_note);
});*/

// make a list of nodes
// 	sorted
//	colored to reflect node state
$.get("node_config.py?p=list_of_nodes&site=poh",function(data) {
	var tmp = $('<ul class="list-group"></ul>');
	$.each(data.list_of_nodes,function(i,node_id) {
		$.get("node_config.py?p=node_name&id=" + node_id,function(data) {
			//tmp.append('<a href="./node-' + ("000" + node_id).slice(-3) + '" class="list-group-item list-group-item-success">' + "Node #" + node_id + " - " + data.node_name + '</a>');
			
			tmp.append('<a href="./node_page/index.php?id=' + node_id + '" id="node' + node_id + '" data-sortby="' + node_id + '" target="_blank" class="list-group-item">' + "Node #" + node_id + " - " + data.node_name + '</a>');
			
			// ajax means results come in with no particular order
			// sort them every time a new entry comes in (a new row is added)
			var ul = $("#poh_nodes > ul");
			var a = ul.children("a");
			a.detach().sort(function(a,b) {
				return $(a).data('sortby') - $(b).data('sortby');
			});
			ul.append(a);
			
			//http://getbootstrap.com/components/#list-group-contextual-classes
			//list-group-item-success
			//list-group-item-info
			//list-group-item-warning
			//list-group-item-danger
			$.get("node_config.py?p=latest_sample&site=poh&id=" + node_id,function(data) {
				// A row is RED if the latest sample from the node was sampled over 30 min ago
				// There is not a row for a node if there is no table/data for that node
				// a row is GREEN otherwise
				if (null === data.latest_sample) {
					$("#node" + node_id).addClass("list-group-item-danger");
					//$("#node" + node_id).addClass("disabled");	// doesn't work - I can still click
					// and it also changes the color back to green...
					//$("#node" + node_id).attr("href","#");
				} else {
					var diff = Date.now()/1000 - data.latest_sample.ReceptionTime;
					if (diff > 30*60) {
						$("#node" + node_id).addClass("list-group-item-danger");
					} else {
						$("#node" + node_id).addClass("list-group-item-success");
					}
				}
			});
		});
	});
	$("#poh_nodes").html(tmp);
});
