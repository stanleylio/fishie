<!DOCTYPE html>
<html lang="en-US">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<!--meta http-equiv="refresh" content="60"-->
		<link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
		<link href="../jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css">
		<script src="../jquery/jquery.min.js" type="text/javascript"></script>
		<script src="../jquery.timeago.js" type="text/javascript"></script>
		
		<link href="node_page.css" rel="stylesheet" type="text/css">

		<?php
			echo "<div id='data-id' data-site=" . $_GET['site'] . " data-node_id=" . $_GET['node_id'] . "></div>";
		?>
	</head>
	<body>
		<div class="container-fluid">
			<div class="page-header row">
				<div class="col-xs-10 col-xs-offset-1">
					<div id="header">
						<h1 id="node_name"></h1>
						<h3 id="node_id"></h3>
						<p id="node_note"></p>
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col-xs-10 col-xs-offset-1">
					<div class="row">
						<div class="col-xs-12 col-sm-3"><p style="font-weight: bold;">Last sampled</p></div>
						<div class="col-xs-12 col-sm-8"><div id="lastsampledts"></div></div>
						<div class="col-xs-12 col-sm-3"><p style="font-weight: bold;">Page generated</p></div>
						<div class="col-xs-12 col-sm-8"><div id="pagegeneratedts"></div></div>
					</div>
				</div>
			</div>
			
			<br>

			<div class="row">
				<div class="col-xs-10 col-xs-offset-1 col-sm-5 col-sm-offset-1">
					<table id="latest_table" class="table table-striped table-hover table-condensed"></table>
				</div>
			</div>

			<br>

			<div class="row">
				<div class="col-xs-10 col-xs-offset-1">
					<div id="static_plots" class="row">
						<!--div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="http://192.168.1.102/node-007/Pressure_BMP180.png">
								<img class="img-responsive" src="Met%20Station%20-%20Node%20%237_files/Pressure_BMP180.png">
								<div class="caption">
									<h4>Pressure_BMP180</h4>
									<p>Generated <time title="ago" datetime="2015-10-09T00:00:08.000Z" class="timeago">22 minutes ago</time></p>
									<p>525 points | 2 days, 19 hours</p>
								</div>
							</a>
						</div-->
						
						<!--div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="../node-007/Pressure_BMP180.png">
								<img class="img-responsive" src="../node-007/Pressure_BMP180.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="../node-007/Temp_BMP180.png">
								<img class="img-responsive" src="../node-007/Temp_BMP180.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>					
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="../node-007/Amb_Si1145.png">
								<img class="img-responsive" src="../node-007/Amb_Si1145.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div-->					
					</div>
				</div>
			</div>
			
			<div class="col-xs-12">
				<div class="text-center" style="color:#C8C8C8; font-size:xx-small;">
					<footer id="footer"></footer>
					<script>$('#footer').load("../footer.html");</script>
				</div>
			</div>
		</div>

		<script src="node_page.js" type="text/javascript"></script>
	</body>
</html>