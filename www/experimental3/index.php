<!DOCTYPE HTML>
<html lang="en-US">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<!--meta http-equiv="refresh" content="60"-->
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<!--script src="https://cdn.plot.ly/plotly-latest.min.js"></script-->
		<script src="plotly-latest.min.js"></script>
		<script src="../jquery/jquery.min.js"></script>
		<title>experimental3</title>
		<!-- http://192.168.0.20/experimental3/?site=poh&node_id=node-009&variable=d2w -->
		<?php
			echo "<div id='data-id' data-site=" . $_GET['site'] . " data-node_id=" . $_GET['node_id'] . " data-variable=" . $_GET['variable'] . "></div>";
		?>
	</head>
	<body>
		<div id="tester" style="width:960px;height:500px;"></div>
		<script src="create_plot.js"></script>
	</body>
</html>