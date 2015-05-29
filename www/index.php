<!DOCTYPE HTML>
<html lang="en-US">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
		<link href="../jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css">
		<script src="../jquery/jquery.min.js" type="text/javascript"></script>
		<script src="../jquery.timeago.js" type="text/javascript"></script>
		
		<link href="node_page.css" rel="stylesheet" type="text/css">
		
		<?php
			// not yet ready for base station and web server deployment. need path to database and configs at least.
		?>
		
		<?php
			// initialize the variables (node id, name, note etc.)
			$dbfile = '../storage/sensor_data.db';
			$node_config_file = '../node_config.ini';
			$display_config_file = '../display_config.ini';
			if (!file_exists($dbfile) || !file_exists($node_config_file) || !file_exists($display_config_file)) {
				echo "<br>";
				echo "debug: database or config file not found. Make sure the following exist:";
				echo "<br>";
				echo $dbfile;
				echo "<br>";
				echo $node_config_file;
				echo "<br>";
				echo $display_config_file;
				echo "<br>";
				exit();
			}

			$ini = parse_ini_file($node_config_file,true,INI_SCANNER_RAW);
			$node_id = $ini['node']['id'];
			$node_tag = sprintf("node_%03d",$node_id);
			$node_name = $ini[$node_tag]['name'];
			$node_note = $ini[$node_tag]['note'];
			
			$table_name = $node_tag;
			$time_col = "Timestamp";
			
			echo "<title>Node #" . $node_id . "</title>";

			// get an associative array of [dbtag=>dbunit]
			function get_tag2unit_map($node_id) {
				$node_tag = sprintf('node_%03d',$node_id);
				$ini = parse_ini_file($GLOBALS['node_config_file'],true,INI_SCANNER_RAW);
				$dbtags = explode(',',$ini[$node_tag]['dbtag']);
				$dbunits = explode(',',$ini[$node_tag]['dbunit']);
				$mapping = array();
				foreach ($dbtags as $k=>$v) {
					$mapping[$v] = $dbunits[$k];
				}
				return $mapping;
			}
			
			// get the unit of the given variable of the given node
			function tag2unit($node_id,$tag) {
				$mapping = get_tag2unit_map($node_id);
				return $mapping[$tag];
			}
		?>
	</head>
	<body>
		<div class="container-fluid">
			<div class="page-header row">
				<div class="col-xs-10 col-xs-offset-1">
					<?php
						echo '<h1>Node #' . $node_id . '</h1>';
						echo '<h3>' . $node_name . '</h3>';
						echo '<p>' . $node_note . '</p>';
					?>
				</div>
			</div>
			
			<div class="row">
				<div class="col-xs-10 col-xs-offset-1">
					<div class="row">
						<?php
							$db = new SQLite3($dbfile,SQLITE3_OPEN_READONLY);
							$query = "SELECT * FROM $table_name ORDER BY $time_col DESC LIMIT 1";
							$result = $db->query($query);
							$latestreading = $result->fetchArray(SQLITE3_ASSOC);
							//var_dump($row[$time_col]);
							//echo "<br><br>";
							//print_r(date_parse($row[$time_col]));
							//echo "<br><br>";
							//print_r(strtotime($row[$time_col]));
							//echo "<br><br>";
							echo "<div class=\"col-xs-12 col-sm-3\"><p style=\"font-weight: bold;\">Last sampled</p></div>";
							echo "<div class=\"col-xs-12 col-sm-8\"><div id=\"lastsampledts\" data-ts=\"" . strtotime($latestreading[$time_col]) . "\"></div></div>";
							echo "<div class=\"col-xs-12 col-sm-3\"><p style=\"font-weight: bold;\">Page generated</p></div>";
							echo "<div class=\"col-xs-12 col-sm-8\"><div id=\"pagegeneratedts\"></div></div>";
						?>
					</div>
				</div>
			</div>

			<br>

			<div id="latest_table" class="row">
				<div class="col-xs-10 col-xs-offset-1 col-sm-5 col-sm-offset-1">
					<table class="table table-striped table-hover table-condensed">
						<?php
							// the list of variables to display
							$ini = parse_ini_file($display_config_file,false,INI_SCANNER_RAW);
							$variables = explode(',',$ini['variable']);
							
							echo "<tr><th>Variable</th><th>Value</th><th>unit</th></tr>";
							foreach ($variables as $tag) {
								$unit = tag2unit($node_id,$tag);
								if (strlen($unit) <= 0) {
									$unit = '-';
								}
								//echo "<tr><td>$tag</td><td>$latestreading[$tag]</td><td>$unit</td></tr>";
								$link = "./experimental2/index.php?tag=" . $tag . "&nhour=24";
								echo "<tr><td><a href=\"$link\" title=\"click for self-updating plot\" target=\"_blank\">$tag</a></td><td>$latestreading[$tag]</td><td>$unit</td></tr>";
							}
						?>
					</table>
				</div>
			</div>

			<br>
			
			<div class="row">
				<div class="col-xs-10 col-xs-offset-1">
					<div class="row">
						<?php
							foreach ($variables as $v) {
								$imgsrc = $table_name . '/' . $v . '.png';
								$link = "./experimental2/index.php?tag=" . $v . "&nhour=24";
								//echo "<a href=\"$link\">$imgsrc</a>";
								//echo "<br>";
								
								$tmp = file_get_contents($table_name . '/' . $v . '.json');
								$json = json_decode($tmp);
								$plot_type = $json->plot_type;
								if ("hourly" === $plot_type) {
									$plot_type = 'Hourly Average';
								} elseif ("daily" === $plot_type) {
									$plot_type = 'Daily Average';
								}
								$plot_generated_at = $json->plot_generated_at;
								$tmp = $json->time_end - $json->time_begin;
								$nday = floor($tmp / (24*60*60));
								$remain = $tmp % (24*60*60);
								$time_span = '';
								if ($nday > 0) {
									$time_span = "$nday days, " . floor($remain/3600) . " hours";
								} else {
									$time_span = floor($remain/3600) . " hours";
								}
								
								// The plot images are of slightly different sizes, and bootstrap doesn't like that.
								// But if I force it by using "row" and put two or three columns depending on width, I
								// may as well do my own layout.
								echo "<div class=\"col-xs-12 col-sm-6 col-lg-4\"><div class=\"staticplot\" data-tag=\"$v\" data-src=\"$imgsrc\" data-link=\"$link\" data-timespan=\"$time_span\" data-plottype=\"$plot_type\" data-generatedat=\"$plot_generated_at\"></div></div>";
							}
						?>
						<!--<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="node_004/EZO_EC.png">
								<img class="img-responsive" src="node_004/EZO_EC.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="node_004/EZO_Sal.png">
								<img class="img-responsive" src="node_004/EZO_Sal.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="node_004/EZO_DO.png">
								<img class="img-responsive" src="node_004/EZO_DO.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="node_004/EZO_pH.png">
								<img class="img-responsive" src="node_004/EZO_pH.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="node_004/EZO_ORP.png">
								<img class="img-responsive" src="node_004/EZO_ORP.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>
						<div class="col-xs-12 col-sm-6 col-lg-4">
							<a class="thumbnail" href="node_004/Pressure_BMP180.png">
								<img class="img-responsive" src="node_004/Pressure_BMP180.png">
								<div class="caption">
									<p>Time span, hourly average, generated N minutes ago</p>
								</div>
							</a>
						</div>-->
					</div>
				</div>
			</div>
			
			<br><br>

			<div class="col-xs-12">
				<div class="text-center" style="color:#C8C8C8; font-size:xx-small;">
					<footer>
						<br><br>
						<p>Stanley Hou In Lio, hlio [at] usc.edu</p>
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
					var d = new Date($(element).attr('data-generatedat')*1000);
					var ts = $('<time></time>').attr('class','timeago').attr('datetime',d.toISOString()).html('ago');
					
					var tmp = $('<a class="thumbnail" target="_blank" href="' + $(element).attr('data-link') + '"></a>')
					.append($('<img class="img-responsive" src="' + $(element).attr('data-src') + '" alt="' + $(element).attr('data-tag') + '"></img>'))
					.append($('<div class="caption"></div>')
					.append('<h4>' + $(element).attr('data-tag') + '</h4>')
					.append($('<p>' + $(element).attr('data-timespan') + ' | ' + $(element).attr('data-plottype') + ' | Generated ' + ts.prop('outerHTML') + '</p>')));
					
					//$('<div class="col-xs-12 col-sm-6 col-lg-4"></div>').append(tmp).appendTo($(element));
					$(element).append(tmp);
					$("time.timeago").timeago();
				});
			});
		</script>
	</body>
</html>