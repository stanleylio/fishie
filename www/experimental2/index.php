<?php
    // Allow from any origin
    if (isset($_SERVER['HTTP_ORIGIN'])) {
        //header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
		header("Access-Control-Allow-Origin: *");
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Max-Age: 86400');    // cache for 1 day
    }

    // Access-Control headers are received during OPTIONS requests
    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers:        {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

        exit(0);
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="../bootstrap/css/bootstrap.min.css">
		<link href="../jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css">
        <link rel="stylesheet" type="text/css" href="index.css">

		<script type="text/javascript" src="../jquery/jquery.min.js"></script>
		<script type="text/javascript" src="../bootstrap/js/bootstrap.min.js"></script>
		<script type="text/javascript" src="../jquery.timeago.js"></script>
		<script type="text/javascript" src="../flot/jquery.flot.min.js"></script>
        <script type="text/javascript" src="../flot/jquery.flot.time.min.js"></script>
		<script type="text/javascript" src="../flot/jquery.flot.selection.min.js"></script>
		<script type="text/javascript" src="../jquery-ui/jquery-ui.min.js"></script>
		<script type="text/javascript" src="../flot/jquery.flot.resize.min.js"></script>
		<script type="text/javascript" src="../jquery.ui.touch-punch.min.js"></script>
		
		<script type="text/javascript" src="plot.js"></script>
		<script type="text/javascript" src="support.js"></script>

		<?php
			$node_config_file = '../../config/node_config.ini';
			$ini = parse_ini_file($node_config_file,true,INI_SCANNER_RAW);

			//print_r($ini);
			//print_r($ini['id']);
		
			$node_id = $ini['node']['id'];
			if (isset($_GET['id'])) {
				$node_id = $_GET{'id'};
			}
			if (isset($_GET['tag'])) {
				$tag = $_GET{'tag'};
			} else {
				echo "must specific name of variable using tag=name";
				exit();
			}
			$nhour = 24;
			if (isset($_GET['nhour'])) {
				$nhour = $_GET{'nhour'};
			}
			
			echo "<title>Node " . $node_id . " - " . $_GET['tag'] . "</title>";
		?>
    </head>
    <body>
		<div class="container-fluid">
			<div class="page-header row">
				<div class="col-xs-12 col-xs-offset-1">
					<div id="header"></div>
				</div>
			</div>
			
			<div class="row">
				<div class="col-sm-10 col-sm-offset-1 testlayout">
					<div id="content"></div>
				</div>
			</div>
			
			<div class="row">
				<div class="col-sm-10 col-sm-offset-1 testlayout">
					<button id="refreshbutton" type="button" class="btn btn-default btn-lg">
						<span class="glyphicon glyphicon-refresh" aria-hidden="true"></span> Refresh 
					</button>
				</div>
			</div>
			<div class="row">
				<div class="col-sm-10 col-sm-offset-1 testlayout">
					<p id="status"></p>
				</div>
			</div>
			
			<?php
				echo "<div id=\"what\" data-id=\"$node_id\" data-tag=\"$tag\" data-nhour=\"$nhour\"></div>";
			?>
			
			<br><br><br>
			
			<script>
				function populate_page(jsonobj) {
					$('#content').html('');
					$('#header').html('');
					
					var node_id = jsonobj.id;
					var node_name = jsonobj.node_name;
					var node_note = jsonobj.node_note;
					var var_datapoints = jsonobj.points;
					
					$('#header').append('<h1>Node #' + node_id + '</h1>');
					$('#header').append('<h3>' + node_name + '</h3>');
					$('#header').append('<p>' + node_note + '</p>');
					$('#header').append('<p>(Plot auto refreshes every minute)</p>');
					
					if (var_datapoints.length <= 0) {
						alert('no data point fits the criteria');
					}
					
					var plotinfo = $('<div class="testlayout"></div>');
					$('<div class="row"></div>')
					.append('<div class="col-xs-12 col-sm-12"><h3>' + jsonobj.description + '</h3></div>').appendTo(plotinfo);
					
					var info = get_plot_info(jsonobj);
					for (var i = 0; i < info.length; i++) {
						$('<div class="row"></div>')
						.append('<div class="col-xs-12 col-sm-3"><p style="font-weight:bold;">' + info[i][0] + '</p></div>')
						.append('<div class="col-xs-12 col-sm-9"><p>' + info[i][1] + '</p></div>')
						.appendTo(plotinfo);
					}

					var plotframe = $('<div class="row"><div class="col-xs-12 col-sm-10 col-sm-offset-1"></div></div>')
					.append(get_plot(jsonobj));

					$('<div class="testlayout"></div>').append(plotinfo).append(plotframe).appendTo('#content');
					
					// rendering
					$("time.timeago").timeago();
					plot_all();
				}
			
				function ajax_refresh() {
					var cutidx = $(location).attr('href').lastIndexOf('/');
					var scripturl = $(location).attr('href').split('?')[0].substring(0,cutidx) + '/fetch_data.py';
					
					$.ajax({	// can use .getJSON() too.
						//url:$(location).attr('href') + '/fetch_data.py',
						url:scripturl,
						type:'GET',
						data: {
							id:$('#what').attr('data-id'),
							tag:$('#what').attr('data-tag'),
							nhour:$('#what').attr('data-nhour'),
							nocache:Math.round(Math.random()*1000000)
						},
						cache:false,
						dataType:'json',
						success:function(jsonobj) {
							populate_page(jsonobj);
						},
						error:function() {
							$('#content').html('<p>AJAX call failed.</p><img src="sobbing.png" />');
						}
					});
				}
				
				$(document).ajaxStart(function() {
					$('#status').html('Retrieving data... (shouldn\'t take more than a minute)');
					$('#refreshbutton').hide();
				});
				
				$(document).ajaxStop(function() {
					$('#refreshbutton').show();
					$('#status').html('');
					
					setTimeout(function() {
						ajax_refresh();
					},60000);
				});
				
				$('#refreshbutton').on('click',function() {
					ajax_refresh();
				});
				
				ajax_refresh();
				
				// can also do a setTimeout() in ajax.Stop(). Ensures that new call is not dispatched before old one finishes
				/*setInterval(function() {
					ajax_refresh();
				},60000);*/
				
			</script>
		</div>
	</body>
</html>
