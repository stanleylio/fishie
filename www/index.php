<!DOCTYPE HTML>
<html lang="en-US">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link href="./bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
		<link href="./jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css">
		<script src="./jquery/jquery.min.js" type="text/javascript"></script>
		<script src="./jquery.timeago.js" type="text/javascript"></script>
		
		<link href="node_page.css" rel="stylesheet" type="text/css">
	</head>
	<body>
		<div class="container-fluid">
			<div class="page-header row">
				<div class="col-xs-10 col-xs-offset-1">
					<div id="header">
						<h2 id="node_name"></h2>
						<p id="node_note"></p>
					</div>
				</div>
			</div>

			<br>

			<div class="row">
				<div class="col-xs-10 col-xs-offset-1 col-md-4">
					<div id="list_of_nodes">placeholder for list of nodes</div>
				</div>
			</div>
			
			<br><br>

			<div class="col-xs-12">
				<div class="text-center" style="color:#C8C8C8; font-size:xx-small;">
					<footer>
						<br><br>
						<p>Stanley Hou In Lio, hlio [at] soest.hawaii.edu</p>
						<p>All Rights Reserved <?php echo date("Y"); ?></p>
						<br>
					</footer>
				</div>
			</div>
		</div>

		<script>
			$(function() {
				// render the timeago elements for Last Sampled At and Page Generated At
				var ts = $('#lastsampledts').attr('data-ts');
				var d = new Date(ts*1000);
				var tmp = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
				//$('<p></p>').append(d.toUTCString()).append(' (' + tmp.prop('outerHTML') + ')')
				//.appendTo('#lastsampledts');
				$('<p></p>').append(tmp.prop('outerHTML')).appendTo('#lastsampledts');
				
				d = new Date(Date.now());
				tmp = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
				//$('<p></p>').append(d.toUTCString()).append(' (' + tmp.prop('outerHTML') + ')')
				//.appendTo('#pagegeneratedts');
				$('<p></p>').append(tmp.prop('outerHTML')).appendTo('#pagegeneratedts');
				
				// render the timeago elements in the caption of every plot
				$("div.staticplot").each(function(index,element) {
					var d = new Date($(element).attr('data-generatedate')*1000);
					var ts = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
					
					var tmp = $('<a class="thumbnail" target="_blank" href="' + $(element).attr('data-link') + '"></a>')
					.append($('<img class="img-responsive" src="' + $(element).attr('data-src') + '" alt="' + $(element).attr('data-tag') + '"></img>'))
					.append($('<div class="caption"></div>')
					.append('<h4>' + $(element).attr('data-tag') + '</h4>')
					.append($('<p>' + $(element).attr('data-timespan') + ' | ' + 'Generated ' + ts.prop('outerHTML') + '</p>')));
					
					//$('<div class="col-xs-12 col-sm-6 col-lg-4"></div>').append(tmp).appendTo($(element));
					$(element).append(tmp);
					$("time.timeago").timeago();
				});
			});
		</script>

		<script src="dashboard.js" type="text/javascript"></script>
	</body>
</html>