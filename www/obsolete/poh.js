// make a list of nodes
// 	sorted
//	colored to reflect node state
(function() {
	var site = 'poh';

	// get the list of nodes of the given site
	$.get("node_config.py?p=list_of_nodes&site=" + site,function(data) {
		var tmp = $('<ul class="list-group"></ul>');
		
		// for each node of that site
		$.each(data.list_of_nodes,function(i,node_id) {
			
			// get its name
			$.get("node_config.py?p=node_name&site=" + site + "&node_id=" + node_id,function(data) {
				
				// make a row for that node
				tmp.append('<a href="./node_page/index.php?site=' + site + '&node_id=' + node_id + '" id="' + node_id + '" data-sortby="' + node_id + '" class="list-group-item">' + node_id + " - " + data.node_name + '</a>');
				
				// sort the list
				// AJAX means result come in no particular order
				// sort them every time a new entry comes in (a new row is added)
				var ul = $("#" + site + "_nodes > ul");
				var a = ul.children("a");
				a.detach().sort(function(a,b) {
					return $(a).data('sortby') > $(b).data('sortby');
				});
				ul.append(a);
				
				// Color the row red if it hasn't been heard for a while
				// Green otherwise
				//http://getbootstrap.com/components/#list-group-contextual-classes
				//list-group-item-success
				//list-group-item-info
				//list-group-item-warning
				//list-group-item-danger
				$.get("node_config.py?p=latest_sample&site=" + site + "&node_id=" + node_id,function(data) {
					if (null === data.latest_sample) {
						$("#node" + node_id).addClass("list-group-item-danger");
						//$("#node" + node_id).addClass("disabled");	// doesn't work - I can still click
						// and it also changes the color back to green...
					} else {
						var diff = Date.now()/1000 - data.latest_sample.Timestamp;
						if ('ReceptionTime' in data.latest_sample) {
							diff = Date.now()/1000 - data.latest_sample.ReceptionTime;
						}
						if (diff < 30*60) {
							$("#" + node_id).addClass("list-group-item-success");
						} else {
							$("#" + node_id).addClass("list-group-item-danger");
						}
					}
				});
			});
		});
		
		$("#" + site + "_nodes").html(tmp);
	});
})();
