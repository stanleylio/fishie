
// or I could take the NlogN hit and sort them...
function boundaries(tp) {
	var oldest = tp[0][0];
	var latest = tp[0][0];
	var oldest_idx = 0;
	var latest_idx = 0;
	for (var i = 0; i < tp.length; i++) {
		var current = tp[i][0];
		if (current > latest) {
			latest = current;
			latest_idx = i;
		}
		if (current < oldest) {
			oldest = current;
			oldest_idx = i;
		}
	}
	return [tp[oldest_idx],tp[latest_idx]];
}

function get_time_span_string(sec) {
	var span = '';
	if (sec < 60) {
		span = sec.toString() + ' seconds';
	} else if (sec < 3600) {
		span = '~' + Math.round(sec/60.) + ' minutes';
	} else if (sec < 24*3600) {
		span = '~' + Math.round(sec/3600.) + ' hours';
	} else {
		span = '~' + Math.round(sec/24./3600.) + ' days';
	}
	return span;
}
