
// coloring node-005 and node-019

//http://getbootstrap.com/components/#list-group-contextual-classes
//list-group-item-success
//list-group-item-info
//list-group-item-warning
//list-group-item-danger

var nodes = [5,19];
$.each(nodes,function(i,node_id){
	$.get("node_config.py?p=latest_sample&site=node-" + ("000" + node_id).slice(-3) + "&id=" + node_id,function(data) {
		if (null === data.latest_sample) {
			$("#node" + node_id).addClass("list-group-item-danger");
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
