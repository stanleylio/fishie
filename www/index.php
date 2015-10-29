<!DOCTYPE HTML>
<html lang="en-US">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta http-equiv="refresh" content="60">
		<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
		<link href="jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css">
		<script src="jquery/jquery.min.js" type="text/javascript"></script>
		<script src="jquery.timeago.js" type="text/javascript"></script>
		
		<!--link href="node_page.css" rel="stylesheet" type="text/css"-->
		<title>Fishpond Monitoring - PoH</title>
	</head>
	<body>
		<div class="container-fluid">
			<div class="page-header row">
				<div class="col-xs-10 col-xs-offset-1">
					<div id="header">
						<h2>Real-time Fishpond Monitoring</h2>
						<h3>Base Station #3</h3>
						<p>Paepae o He'eia</p>
					</div>
				</div>
			</div>

			<br>

			<div class="row">
				<div class="col-xs-10 col-xs-offset-1 col-md-4">
					<div id="list_of_nodes">list of nodes</div>
				</div>
			</div>
			
			<br><br>

			<div class="row">
				<div class="col-xs-10 col-xs-offset-1 col-md-4">
					<div id="bench_nodes">
						<ul class="list-group">
							<a href="./node_page/index.php?id=5" id="node5" data-sortby="5" target="_blank" class="list-group-item">Node #5 - Lab Ref.</a>
							<a href="./node_page/index.php?id=19" id="node19" data-sortby="19" target="_blank" class="list-group-item">Node #19 - SL personal</a>
						</ul>
					</div>
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

		<script src="dashboard.js" type="text/javascript"></script>
	</body>
</html>