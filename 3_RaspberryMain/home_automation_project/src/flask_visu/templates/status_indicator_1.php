<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
 <link rel="stylesheet" href="./CSS_data/led_lights.css">
 <link rel="stylesheet" href="./CSS_data/slider_style1.css">
 <link rel="stylesheet" type="text/css" href="./CSS_data/general_style.css">
 <link rel="stylesheet" href="./CSS_data/button1_style.css">
  
 <link rel="stylesheet" type="text/css" href="./CSS_data/button2_style/font-awesome.css" > 
 
 <link rel="stylesheet"  href="./CSS_data/style_przycisk.css" >
 <link rel="stylesheet"  href="./CSS_data/button_color.css" >
 <link rel="stylesheet"  href="./CSS_data/dropdown.css" >
 
 <script src="//cdn.rawgit.com/Mikhus/canvas-gauges/gh-pages/download/2.1.7/all/gauge.min.js"></script>
 
</head>

<body>

<h1 style="font-family: courier;" align="center">HOME Automation System</h1>


<!-- show outdoor temperature -->
<div style="position:relative; left:15px; top:20px"> 
	<p class="a" style="position:relative;width:350px; left:5px; font-family:courier" >Outdoor Temperature</p> 
	<div id="gauge1_1" style="width: 100px; height: 50px"></div>
</div>

<!-- show outdoor humidity -->
<div style="position:relative; left:210px; top:-50px"> 
	<p class="a" style="position:relative;width:350px; left:10px; font-family:courier" >Outdoor Humidity</p> 
	<div id="gauge1_2" style="width: 100px; height: 50px"></div>
</div>  

<!-- show outdoor pressure -->
<div style="position:relative; left:705px; top:-120px"> 
	<p class="a" style="position:relative;width:350px; left:40px; font-family:courier" >Pressure</p> 
	<div id="gauge1_3" style="width: 100px; height: 50px"></div>
</div> 

<!-- display the pressure chart -->
<div id="pressure_chart" style="position:relative; left:550px; top: -10px; width: 550px; height: 280px"></div>

<!-- display the temperature&humidity chart -->
<div id="curve_chart1" style="position:relative; left:30px; top: -290px; width: 550px; height: 280px"></div>


<!-- Outdoor temp&humidity dropdown time window-->
<div class="dropdown" style="position:absolute; left:300px; top: 230px; font-family:courier" >
	<button >Time Window</button>
	<div class="dropdown-content">
	<a href="#" onClick="redrawChart_1day();">1 day</a>
	<a href="#" onClick="redrawChart_1week();">1 week</a>
	<a href="#" onClick="redrawChart_1month();">1 month</a>
	<a href="#" onClick="redrawChart();">Redraw: 6h</a>
	</div>	  	  
</div>
 

<!-- L1,L2,L3 current gauges -->
<div style="position:relative; left:20px; top:-280px"> 
	<p class="a" style="position:relative;width:300px; top:10px; left:90px; font-family:courier" >L1,L2,L3 current measurement</p> 
	<div id="Current_Meas" style="width: 100px; height: 50px; position: relative; top:15px"></div>
</div>

<!-- display the curent L1,L2,L3 chart -->
<div id="Current_Meas_chart" style="position:relative; left:50px; top: -170px; width: 500px; height: 210px"></div>

<!-- Current L1 L2 L3 dropdown time window-->
<div class="dropdown" style="position:absolute; left:400px; top: 680px; font-family:courier" >
	<button >Time Window</button>
	<div class="dropdown-content">
	<a href="#" onClick="redrawCurrent_Chart_1day();">1 day</a>
	<a href="#" onClick="redrawCurrent_Chart_1week();">1 week</a>
	<a href="#" onClick="redrawCurrent_Chart_1month();">1 month</a>
	<a href="#" onClick="redrawCurrent_Chart();">Redraw: 6h</a>
	</div>	  	  
</div>

<!-- display air pollution PM1 indoor -->
<!--
<div style="position:relative; left:1200px; top:-750px"> 
	<p class="a" style="position:relative;width:350px; left:40px; font-family:courier" >PM 1 Indoor</p> 
	<div id="gauge1_5" style="width: 100px; height: 50px"></div>
</div> 
-->

<!-- display air pollution PM1 outdoor -->
<!--
<div style="position:relative; left:1400px; top:-820px"> 
	<p class="a" style="position:relative;width:350px; left:40px; font-family:courier" >PM 1 Outdoor</p> 
	<div id="gauge1_6" style="width: 100px; height: 50px"></div>
</div> 
-->



<div style="position:absolute; left:1150px; top:70px"> 
	<canvas id="gauge_PM1_in"
			data-value-box="true" ></canvas>
</div> 

<div style="position:absolute; left:1500px; top:70px"> 
	<canvas id="gauge_PM1_out"
			data-value-box="true" ></canvas>
</div> 

<div style="position:absolute; left:1150px; top:350px"> 
	<canvas id="gauge_PM2_5_in"
			data-value-box="true" ></canvas>
</div> 

<div style="position:absolute; left:1500px; top:350px"> 
	<canvas id="gauge_PM2_5_out"
			data-value-box="true" ></canvas>
</div> 

<div style="position:absolute; left:1150px; top:650px"> 
	<canvas id="gauge_PM10_in"
			data-value-box="true" ></canvas>
</div> 

<div style="position:absolute; left:1500px; top:650px"> 
	<canvas id="gauge_PM10_out"
			data-value-box="true" ></canvas>
</div>


<!--Navigation button  -->
<div style="position:absolute; left:700px; top: 750px; font-family:courier; width: 100px;" >
	<button class="w3-button w3-cyan" onclick="window.location.href='status_indicator_2.php';"  > Next Rooms </button>
</div> 


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script src="jquery.min.js"></script>
<script type="text/javascript">

	  // draw gauge visualizations  
	  google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawVisualization);
	  
	  google.charts.load('current', {'packages':['corechart']});
	  google.charts.setOnLoadCallback(drawChart);
	  google.charts.setOnLoadCallback(drawCurrent_Chart);
	  google.charts.setOnLoadCallback(drawPressureChart);
	  
	  $(document).ready(function() {
		  	
	});	

	  
// draw gauges
function drawVisualization() {
		
		 // outdoor temperature
		data1_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
	      ['Temp.', 0],
        ]);
		
		options1_1 = {
          width: 300, height: 150,
          max:50, min:-30,
          animation:{duration: 400},
	      greenColor:'#08E3E8',
          redFrom:20, redTo:50,
          yellowFrom:0, yellowTo:20,
          greenFrom:-30, greenTo:0,
          minorTicks: 5,
          majorTicks: [-30,-20,-10,0,10,20,30,40,50]
        };
		
        chart1_1 = new google.visualization.Gauge(document.getElementById('gauge1_1'));
 
		// outdoor humidity
		data1_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
	      ['Humid.', 0],
        ]);
 
        options1_2 = {
          width: 300, height: 150,
          max:100, min:0,
          animation:{duration: 400},
	      greenColor:'#08E3E8',
          //redFrom:20, redTo:50,
          //yellowFrom:0, yellowTo:20,
          greenFrom:0, greenTo:100,
          minorTicks: 5,
          majorTicks: [0,10,20,30,40,50,60,70,80,90,100]
        };
		
        chart1_2 = new google.visualization.Gauge(document.getElementById('gauge1_2'));
		
		// outdoor pressure
		data1_3 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
	      ['Press.[hPa]', 0],
        ]);
		
		options1_3 = {
          width: 300, height: 150,
          max:1100, min:850,
          animation:{duration: 400},
	      greenColor:'#00FF40',
          //redFrom:20, redTo:50,
          //yellowFrom:0, yellowTo:20,
          greenFrom:850, greenTo:1100,
          minorTicks: 5,
          majorTicks: [850,900,950,1000,1050,1100]
        };
		
        chart1_3 = new google.visualization.Gauge(document.getElementById('gauge1_3'));
 
		// L1,L2,L3 current gauges
		data2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
	      ['L1[A]', 0],
	      ['L2[A]', 0],
		  ['L3[A]', 0],
        ]);
 
        options2 = {
          width: 400, height: 200,
          max:20, min:0,
          animation:{duration: 400},
		  greenColor:'#08E3E8',
		  yellowColor: 'FFFF00',
		  redColor: 'FF0000',
          redFrom:18, redTo:20,
          yellowFrom:0, yellowTo:0,
          greenFrom:0, greenTo:0,
          minorTicks: 1,
          majorTicks: [0,2,4,6,8,10,12,14,16,18,20]
        };
		
		chart2 = new google.visualization.Gauge(document.getElementById('Current_Meas'));
 
	
		// room 2 - temperature gauge
		data4_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options4_1 = {
          width: 180, height: 150,
          max:50, min:-30,
          animation:{duration: 400},
	    greenColor:'#08E3E8',
          redFrom:20, redTo:50,
          yellowFrom:0, yellowTo:20,
          greenFrom:-30, greenTo:0,
          minorTicks: 5,
          majorTicks: [-30,-20,-10,0,10,20,30,40,50]
        };
		
		chart4_1 = new google.visualization.Gauge(document.getElementById('gauge4_1'));
 
		// room 2 - humidity gauge
		data4_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid', 0],
        ]);
 
        options4_2 = {
          width: 180, height: 150,
          max:100, min:0,
          animation:{duration: 400},
	    greenColor:'#08E3E8',
          //redFrom:20, redTo:50,
          //yellowFrom:0, yellowTo:20,
          greenFrom:0, greenTo:100,
          minorTicks: 5,
          majorTicks: [0,10,20,30,40,50,60,70,80,90,100]
        };
		
		chart4_2 = new google.visualization.Gauge(document.getElementById('gauge4_2'));
		
        chart1_1.draw(data1_1, options1_1);
		chart1_2.draw(data1_2, options1_2);
		chart1_3.draw(data1_3, options1_3);
		chart2.draw(data2, options2);
		//chart3_1.draw(data3_1, options3_1);
		//chart3_2.draw(data3_2, options3_2);
		//chart4_1.draw(data4_1, options4_1);
		//chart4_2.draw(data4_2, options4_2);
		
		
							   	   }
								   
							   							   
function drawChart() {
		// temperature and humidity chart	
		  var data = new google.visualization.arrayToDataTable([
			
			//data.addColumn(type, label); type=string,number,boolean, date, datetime, timeofday
			//data.addColumn('datetime', 'Timestamp');
			//data.addColumn('number', 'Temperature');
			//data.addColumn('number', 'Humidity');
			
			// data.addRows([
			['Timestamp', 'Temperature', 'Humidity'],
			<?php
						  //$db_host='localhost';
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
						
						   // 6 hours = (6h*60min) / 3min[update cycle into DB] = 120 
						  //$sqlQuery = "SELECT  Timestamp, Temperature, Humidity  FROM GENERAL ORDER BY Timestamp DESC LIMIT 120";
						  $sqlQuery = "SELECT  * FROM GENERAL ORDER BY Timestamp DESC LIMIT 120";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								//printf("row 1 row 2:", $row[0], $row[1]);
								echo "['" . $row['Timestamp'] . "',
								" . $row['Temperature'] . ",
								" . $row['Humidity'] . "],";

								//echo "[" . (float)$row['Temperature'] . ",
								//" . $row['Humidity'] . "],";
						  }
						  
						  mysql_close($db);
						

			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:3,
		  series: {
					0:{color: 'blue', visibleInLegend: true },
					1:{color: 'red', visibleInLegend: true}
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:-15, max:100}, ticks: [-15,-10,-5,0,5,10,15,20,25,30,40,50,60,80,100], title:'°C/%', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart1'));

        chart.draw(data, options);
		
								
				}
//****************************************************************************

//****************************************************************************

function redrawChart_1day() {
								data =  google.visualization.arrayToDataTable([
			
								//data.addColumn(type, label); type=string,number,boolean, date, datetime, timeofday
								//data.addColumn('datetime', 'Timestamp');
								//data.addColumn('number', 'Temperature');
								//data.addColumn('number', 'Humidity');
								
								// data.addRows([
								['Timestamp', 'Temperature', 'Humidity'],
								<?php
											  $db_host='192.168.1.165';
											  $db_database='home_automation_DB';
											  $db_user='mysql_user';
											  $db_password='internet1';
											  
											  $db=mysql_connect($db_host, $db_user, $db_password);
											  if (!$db) {
												die('could not connect to database: '.mysql_error($db));
											   }
											   
											  mysql_select_db($db_database);
											
											  // 1 day = (24h*60min) / 3min[update cycle into DB] = 480 
											  $sqlQuery = "SELECT * FROM GENERAL ORDER BY Timestamp DESC LIMIT 480";
											  $sqlResult = mysql_query($sqlQuery);
											  
											  $array = array();
											  while( $row = mysql_fetch_array($sqlResult))    
											  {  
													//printf("row 1 row 2:", $row[0], $row[1]);
													echo "['" . $row['Timestamp'] . "',
													" . $row['Temperature'] . ",
													" . $row['Humidity'] . "],";

													//echo "[" . (float)$row['Temperature'] . ",
													//" . $row['Humidity'] . "],";
											  }
											  
											  mysql_close($db);
											

								?>
							//	]);
							
								]);
								
							
							   var options = {
							  //title: '',
							  curveType: 'function',
							  chartArea:{width:'80%', height:'70%'},
							  //height:300,
							  lineWidth:3,
							  series: {
										0:{color: 'blue', visibleInLegend: true },
										1:{color: 'red', visibleInLegend: true}
									  },
							  legend: { position: 'top' }, //bottom
							  
							  vAxis: { viewWindow: {min:-15, max:100}, ticks: [-15,-10,-5,0,5,10,15,20,25,30,40,50,60,80,100], title:'°C/%', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
							  
							  //direction:-1 (reverse the order of values)
							  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
							 
							};
							
								var chart = new google.visualization.LineChart(document.getElementById('curve_chart1'));
								
								chart.draw(data, options);
								}


//****************************************************************************
//****************************************************************************
function redrawChart_1week() {
								data =  google.visualization.arrayToDataTable([
			
								//data.addColumn(type, label); type=string,number,boolean, date, datetime, timeofday
								//data.addColumn('datetime', 'Timestamp');
								//data.addColumn('number', 'Temperature');
								//data.addColumn('number', 'Humidity');
								
								// data.addRows([
								['Timestamp', 'Temperature', 'Humidity'],
								<?php
											  $db_host='192.168.1.165';
											  $db_database='home_automation_DB';
											  $db_user='mysql_user';
											  $db_password='internet1';
											  
											  $db=mysql_connect($db_host, $db_user, $db_password);
											  if (!$db) {
												die('could not connect to database: '.mysql_error($db));
											   }
											   
											  mysql_select_db($db_database);
											
											  // 1week = 7d*24h*60min / 3min[update cycle into DB] = 3360
											  //$sqlQuery = "SELECT  Timestamp, Temperature, Humidity  FROM GENERAL ORDER BY Timestamp DESC LIMIT 3360";
											  $sqlQuery = "SELECT  *  FROM GENERAL ORDER BY Timestamp DESC LIMIT 1000";
											  $sqlResult = mysql_query($sqlQuery);
											  
											  $array = array();
											  while( $row = mysql_fetch_array($sqlResult))    
											  {  
													//printf("row 1 row 2:", $row[0], $row[1]);
													echo "['" . $row['Timestamp'] . "',
													" . $row['Temperature'] . ",
													" . $row['Humidity'] . "],";

													//echo "[" . (float)$row['Temperature'] . ",
													//" . $row['Humidity'] . "],";
											  }
											  
											  mysql_close($db);
											

								?>
							//	]);
							
								]);
								
							
							   var options = {
							  //title: '',
							  curveType: 'function',
							  chartArea:{width:'80%', height:'70%'},
							  //height:300,
							  lineWidth:3,
							  series: {
										0:{color: 'blue', visibleInLegend: true },
										1:{color: 'red', visibleInLegend: true}
									  },
							  legend: { position: 'top' }, //bottom
							  
							  vAxis: { viewWindow: {min:-15, max:100}, ticks: [-15,-10,-5,0,5,10,15,20,25,30,40,50,60,80,100], title:'°C/%', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
							  
							  //direction:-1 (reverse the order of values)
							  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
							 
							};
								
								var chart = new google.visualization.LineChart(document.getElementById('curve_chart1'));
								
								chart.draw(data, options);
								}
								
      	
//****************************************************************************
//****************************************************************************
function redrawChart_1month() {
								data =  google.visualization.arrayToDataTable([
			
								//data.addColumn(type, label); type=string,number,boolean, date, datetime, timeofday
								//data.addColumn('datetime', 'Timestamp');
								//data.addColumn('number', 'Temperature');
								//data.addColumn('number', 'Humidity');
								
								// data.addRows([
								['Timestamp', 'Temperature', 'Humidity'],
								<?php
											  $db_host='192.168.1.165';
											  $db_database='home_automation_DB';
											  $db_user='mysql_user';
											  $db_password='internet1';
											  
											  $db=mysql_connect($db_host, $db_user, $db_password);
											  if (!$db) {
												die('could not connect to database: '.mysql_error($db));
											   }
											   
											  mysql_select_db($db_database);
											  
											  // 1month = 30d*24h*60min / 3min[update cycle into DB] = 14400
											  //$sqlQuery = "SELECT  Timestamp, Temperature, Humidity  FROM GENERAL ORDER BY Timestamp DESC LIMIT 14400";
											  $sqlQuery = "SELECT  * FROM GENERAL ORDER BY Timestamp DESC LIMIT 2000";
											  $sqlResult = mysql_query($sqlQuery);
											  
											  $array = array();
											  while( $row = mysql_fetch_array($sqlResult))    
											  {  
													//printf("row 1 row 2:", $row[0], $row[1]);
													echo "['" . $row['Timestamp'] . "',
													" . $row['Temperature'] . ",
													" . $row['Humidity'] . "],";

													//echo "[" . (float)$row['Temperature'] . ",
													//" . $row['Humidity'] . "],";
											  }
											  
											  mysql_close($db);
											

								?>
							//	]);
							
								]);
								
							
							   var options = {
							  //title: '',
							  curveType: 'function',
							  chartArea:{width:'80%', height:'70%'},
							  //height:300,
							  lineWidth:3,
							  series: {
										0:{color: 'blue', visibleInLegend: true },
										1:{color: 'red', visibleInLegend: true}
									  },
							  legend: { position: 'top' }, //bottom
							  
							  vAxis: { viewWindow: {min:-15, max:100}, ticks: [-15,-10,-5,0,5,10,15,20,25,30,40,50,60,80,100], title:'°C/%', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
							  
							  //direction:-1 (reverse the order of values)
							  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
							 
							};
								
								var chart = new google.visualization.LineChart(document.getElementById('curve_chart1'));
								
								chart.draw(data, options);
								
								}
									

//****************************************************************************

//****************************************************************************
function redrawChart() {
								data =  google.visualization.arrayToDataTable([
			
								//data.addColumn(type, label); type=string,number,boolean, date, datetime, timeofday
								//data.addColumn('datetime', 'Timestamp');
								//data.addColumn('number', 'Temperature');
								//data.addColumn('number', 'Humidity');
								
								// data.addRows([
								['Timestamp', 'Temperature', 'Humidity'],
								<?php
											  $db_host='192.168.1.165';
											  $db_database='home_automation_DB';
											  $db_user='mysql_user';
											  $db_password='internet1';
											  
											  $db=mysql_connect($db_host, $db_user, $db_password);
											  if (!$db) {
												die('could not connect to database: '.mysql_error($db));
											   }
											   
											  mysql_select_db($db_database);
											
											  // last 6 hours = 6h*60min / 3min[update cycle into DB] = 120
											  $sqlQuery = "SELECT  *  FROM GENERAL ORDER BY Timestamp DESC LIMIT 120";
											  $sqlResult = mysql_query($sqlQuery);
											  
											  $array = array();
											  while( $row = mysql_fetch_array($sqlResult))    
											  {  
													//printf("row 1 row 2:", $row[0], $row[1]);
													echo "['" . $row['Timestamp'] . "',
													" . $row['Temperature'] . ",
													" . $row['Humidity'] . "],";

													//echo "[" . (float)$row['Temperature'] . ",
													//" . $row['Humidity'] . "],";
											  }
											  
											  mysql_close($db);
											

								?>
							//	]);
							
								]);
								
							
							   var options = {
							  //title: '',
							  curveType: 'function',
							  chartArea:{width:'80%', height:'70%'},
							  //height:300,
							  lineWidth:3,
							  series: {
										0:{color: 'blue', visibleInLegend: true },
										1:{color: 'red', visibleInLegend: true}
									  },
							  legend: { position: 'top' }, //bottom
							  
							  vAxis: { viewWindow: {min:-15, max:100}, ticks: [-15,-10,-5,0,5,10,15,20,25,30,40,50,60,80,100], title:'°C/%', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
							  
							  //direction:-1 (reverse the order of values)
							  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
							 
							};
								
								var chart = new google.visualization.LineChart(document.getElementById('curve_chart1'));
								
								chart.draw(data, options);
								
								}

//****************************************************************************
//****************************************************************************
//****************************************************************************

function drawCurrent_Chart() {
		// current L1 L2 L3 chart	
		  var data = new google.visualization.arrayToDataTable([
			
			// data.addRows([
			['Timestamp', 'Current L1', 'Current L2', 'Current L3'],
			<?php
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
						
						  // last 6 hours = 6h*60min / 10s[update cycle into DB] = 2160
						  //$sqlQuery = "SELECT  Timestamp, Current_L1, Current_L2, Current_L3  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 2160";
						  $sqlQuery = "SELECT  *  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 500";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								//printf("row 1 row 2:", $row[0], $row[1]);
								echo "['" . $row['Timestamp'] . "',
								" . $row['Current_L1'] . ",
								" . $row['Current_L2'] . ",
								" . $row['Current_L3'] . "],";

								//echo "[" . (float)$row['Temperature'] . ",
								//" . $row['Humidity'] . "],";
						  }
						  
						  mysql_close($db);
						

			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:2,
		  series: {
					0:{color: 'green', visibleInLegend: true },
					1:{color: 'violet', visibleInLegend: true},
					2:{color: 'orange', visibleInLegend: true}
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:0, max:20}, ticks: [0,2,4,6,8,10,12,14,16,18,20], title:'[A]', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('Current_Meas_chart'));

        chart.draw(data, options);
								
				}
//*****************************************************************************************************

function redrawCurrent_Chart_1day(){
	// current L1 L2 L3 chart for last one day	
		  var data = new google.visualization.arrayToDataTable([
			
			// data.addRows([
			['Timestamp', 'Current L1', 'Current L2', 'Current L3'],
			<?php
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
							//43200
						  //$sqlQuery = "SELECT  Timestamp, Current_L1, Current_L2, Current_L3  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 8640";
						  $sqlQuery = "SELECT  *  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 1000";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								echo "['" . $row['Timestamp'] . "',
								" . $row['Current_L1'] . ",
								" . $row['Current_L2'] . ",
								" . $row['Current_L3'] . "],";
						  }
						  
						  mysql_close($db);
						

			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:2,
		  series: {
					0:{color: 'green', visibleInLegend: true },
					1:{color: 'violet', visibleInLegend: true},
					2:{color: 'orange', visibleInLegend: true}
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:0, max:20}, ticks: [0,2,4,6,8,10,12,14,16,18,20], title:'[A]', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('Current_Meas_chart'));

        chart.draw(data, options);
	
}

//***************************************************************************************************************

function redrawCurrent_Chart_1week(){
	// current L1 L2 L3 chart for last one day	
		  var data = new google.visualization.arrayToDataTable([
			
			// data.addRows([
			['Timestamp', 'Current L1', 'Current L2', 'Current L3'],
			<?php
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
							//302400
						  //$sqlQuery = "SELECT  Timestamp, Current_L1, Current_L2, Current_L3  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 60480";
						  $sqlQuery = "SELECT  *  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 1500";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								echo "['" . $row['Timestamp'] . "',
								" . $row['Current_L1'] . ",
								" . $row['Current_L2'] . ",
								" . $row['Current_L3'] . "],";
						  }
						  
						  mysql_close($db);
						  
			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:2,
		  series: {
					0:{color: 'green', visibleInLegend: true },
					1:{color: 'violet', visibleInLegend: true},
					2:{color: 'orange', visibleInLegend: true}
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:0, max:20}, ticks: [0,2,4,6,8,10,12,14,16,18,20], title:'[A]', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('Current_Meas_chart'));

        chart.draw(data, options);
	
}

//***************************************************************************************************************

function redrawCurrent_Chart_1month(){
	// current L1 L2 L3 chart for last one day	
		  var data = new google.visualization.arrayToDataTable([
			
			// data.addRows([
			['Timestamp', 'Current L1', 'Current L2', 'Current L3'],
			<?php
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
							//1296000
						  $sqlQuery = "SELECT  *  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 2000";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								echo "['" . $row['Timestamp'] . "',
								" . $row['Current_L1'] . ",
								" . $row['Current_L2'] . ",
								" . $row['Current_L3'] . "],";
						  }
						  
						  mysql_close($db);
						  
			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:2,
		  series: {
					0:{color: 'green', visibleInLegend: true },
					1:{color: 'violet', visibleInLegend: true},
					2:{color: 'orange', visibleInLegend: true}
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:0, max:20}, ticks: [0,2,4,6,8,10,12,14,16,18,20], title:'[A]', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('Current_Meas_chart'));

        chart.draw(data, options);
	
}

//***************************************************************************************************************

function redrawCurrent_Chart(){
		// current L1 L2 L3 chart	
		  data = google.visualization.arrayToDataTable([
			
			// data.addRows([
			['Timestamp', 'Current L1', 'Current L2', 'Current L3'],
			<?php
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
							//10800
						  $sqlQuery = "SELECT  *  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 500";
						  //$sqlQuery = "SELECT  Timestamp, Current_L1, Current_L2, Current_L3  FROM CURRENT_MEAS ORDER BY Timestamp DESC LIMIT 120";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								//printf("row 1 row 2:", $row[0], $row[1]);
								echo "['" . $row['Timestamp'] . "',
								" . $row['Current_L1'] . ",
								" . $row['Current_L2'] . ",
								" . $row['Current_L3'] . "],";

								//echo "[" . (float)$row['Temperature'] . ",
								//" . $row['Humidity'] . "],";
						  }
						  
						  mysql_close($db);
						

			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:2,
		  series: {
					0:{color: 'green', visibleInLegend: true },
					1:{color: 'violet', visibleInLegend: true},
					2:{color: 'orange', visibleInLegend: true}
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:0, max:20}, ticks: [0,2,4,6,8,10,12,14,16,18,20], title:'[A]', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('Current_Meas_chart'));

        chart.draw(data, options);

}


function drawPressureChart() {
		// Pressure chart	
		  var data = new google.visualization.arrayToDataTable([
			
			//data.addColumn(type, label); type=string,number,boolean, date, datetime, timeofday
			//data.addColumn('datetime', 'Timestamp');
			//data.addColumn('number', 'Temperature');
			//data.addColumn('number', 'Humidity');
			
			// data.addRows([
			['Timestamp', 'Pressure'],
			<?php
						  //$db_host='localhost';
						  $db_host='192.168.1.165';
						  $db_database='home_automation_DB';
						  $db_user='mysql_user';
						  $db_password='internet1';
						  
						  $db=mysql_connect($db_host, $db_user, $db_password);
						  if (!$db) {
							die('could not connect to database: '.mysql_error($db));
						   }
						   
						  mysql_select_db($db_database);
						
						   // 6 hours = (6h*60min) / 3min[update cycle into DB] = 120 
						  //$sqlQuery = "SELECT  Timestamp, Temperature, Humidity  FROM GENERAL ORDER BY Timestamp DESC LIMIT 120";
						  $sqlQuery = "SELECT  * FROM GENERAL ORDER BY Timestamp DESC LIMIT 120";
						  $sqlResult = mysql_query($sqlQuery);
						  
						  $array = array();
						  while( $row = mysql_fetch_array($sqlResult))    
						  {  
								//printf("row 1 row 2:", $row[0], $row[1]);
								echo "['" . $row['Timestamp'] . "',
								" . $row['Pressure'] . "],";

								//echo "[" . (float)$row['Temperature'] . ",
								//" . $row['Humidity'] . "],";
						  }
						  
						  mysql_close($db);
						

			?>
		//	]);
		
			]);
			
		
		   var options = {
          //title: '',
          curveType: 'function',
		  chartArea:{width:'80%', height:'70%'},
		  //height:300,
		  lineWidth:3,
		  series: {
					0:{color: '#00FF00', visibleInLegend: true }
		          },
          legend: { position: 'top' }, //bottom
		  
		  vAxis: { viewWindow: {min:970, max:1050}, ticks: [970,980,990,1000,1010,1020,1030,1040,1050], title:'hPa', titleTextStyle: {fontSize:15, italic:false}, slantedText: true, slantedTextAngle: 90},
		  
		  //direction:-1 (reverse the order of values)
		  hAxis: { direction:-1, textStyle: {fontSize:9}, slantedText:true, slantedTextAngle:90 }
		 
        };

        var chart = new google.visualization.LineChart(document.getElementById('pressure_chart'));

        chart.draw(data, options);
		
								
				}

//*****************************************************************************************************
  							      
function test(ajaxdata) {
		var Temp_Room1=ajaxdata.Temp_Room1_AJAX;
		var Temp_Room2=ajaxdata.Temp_Room2_AJAX;
		var Temp_Room3=ajaxdata.Temp_Room3_AJAX;
		var Temp_Room4=ajaxdata.Temp_Room4_AJAX;
		var Temp_Room5=ajaxdata.Temp_Room5_AJAX;

		var Humid_Room1=ajaxdata.Humid_Room1_AJAX;
		var Humid_Room2=ajaxdata.Humid_Room2_AJAX;
		var Humid_Room3=ajaxdata.Humid_Room3_AJAX;
		var Humid_Room4=ajaxdata.Humid_Room4_AJAX;
		var Humid_Room5=ajaxdata.Humid_Room5_AJAX;
		
		var Temp_Outdoor=ajaxdata.Temp_Outdoor_AJAX;
		var Humid_Outdoor=ajaxdata.Humid_Outdoor_AJAX;
		var Press_Outdoor=ajaxdata.Press_Outdoor_AJAX;
		
		var PM1_Outdoor  =ajaxdata.PM1_Outdoor_AJAX;
		var PM2_5_Outdoor=ajaxdata.PM2_5_Outdoor_AJAX;
		var PM10_Outdoor =ajaxdata.PM10_Outdoor_AJAX;
		
		var PM1_Indoor  =ajaxdata.PM1_Indoor_AJAX;
		var PM2_5_Indoor=ajaxdata.PM2_5_Indoor_AJAX;
		var PM10_Indoor =ajaxdata.PM10_Indoor_AJAX;
		
		var Current_L1=ajaxdata.Current_L1_AJAX;
		var Current_L2=ajaxdata.Current_L2_AJAX;
		var Current_L3=ajaxdata.Current_L3_AJAX;
		
		var Motion_Sensor1=ajaxdata.MotionSensor1_AJAX; 
		var Motion_Sensor2=ajaxdata.MotionSensor2_AJAX;
		var Motion_Sensor3=ajaxdata.MotionSensor3_AJAX;
		var Motion_Sensor4=ajaxdata.MotionSensor4_AJAX;
		var Motion_Sensor5=ajaxdata.MotionSensor5_AJAX;
		
		var Smoke_Sensor3=ajaxdata.SmokeSensor3_AJAX;
		
// *************************************************
		var gauge_PM1_in = new LinearGauge({
		renderTo: 'gauge_PM1_in',
		width: 320,
		height: 100,
		units: "",
		title: "PM1 indoor [ug/m3]",
		minValue: 0,
		maxValue: 160,
		majorTicks: [0,20,40,60,80,100,120,140,160],
		minorTicks: 5,
		strokeTicks: true,
		ticksWidth: 15,
		ticksWidthMinor: 7.5,
		highlights: [
        {
            "from": 0,
            "to": 40,
            "color": "rgba(29,239, 77, .9)"
        },
        {
            "from": 40,
            "to": 100,
            "color": "rgba(253, 126, 0, .9)"
        },
		{
            "from": 100,
            "to": 160,
            "color": "rgba(230, 0, 0, .9)"
        }
    ],
    colorMajorTicks: "#000000",
    colorMinorTicks: "#000000",
    colorTitle: "#000000",
    colorUnits: "#000000",
    colorNumbers: "#000000",
    colorPlate: "#ffffff",
    colorPlateEnd: "#ffffff",
    borderShadowWidth: 0,
    borders: false,
    borderRadius: 10,
    needleType: "arrow",
    needleWidth: 1,
	valueBox: true,
	animation: false,
    animationDuration: 100,
    animationRule: "linear",
    colorNeedle: "#3f48cc",
    colorNeedleEnd: "#3f48cc",
    colorBarProgress: "#327ac0",
    colorBar: "#f5f5f5",
    barStroke: 0,
    barWidth: 15,
    barBeginCircle: false
});
	

	gauge_PM1_in.value = PM1_Indoor;
	gauge_PM1_in.draw();

	var gauge_PM1_out = new LinearGauge({
		renderTo: 'gauge_PM1_out',
		width: 320,
		height: 100,
		units: "",
		title: "PM1 outdoor [ug/m3]",
		minValue: 0,
		maxValue: 160,
		majorTicks: [0,20,40,60,80,100,120,140,160],
		minorTicks: 5,
		strokeTicks: true,
		ticksWidth: 15,
		ticksWidthMinor: 7.5,
		highlights: [
        {
            "from": 0,
            "to": 40,
            "color": "rgba(29,239, 77, .9)"
        },
        {
            "from": 40,
            "to": 100,
            "color": "rgba(253, 126, 0, .9)"
        },
		{
            "from": 100,
            "to": 160,
            "color": "rgba(230, 0, 0, .9)"
        }
    ],
    colorMajorTicks: "#000000",
    colorMinorTicks: "#000000",
    colorTitle: "#000000",
    colorUnits: "#000000",
    colorNumbers: "#000000",
    colorPlate: "#ffffff",
    colorPlateEnd: "#ffffff",
    borderShadowWidth: 0,
    borders: false,
    borderRadius: 10,
    needleType: "arrow",
    needleWidth: 1,
	valueBox: true,
	animation: false,
    animationDuration: 100,
    animationRule: "linear",
    colorNeedle: "#3f48cc",
    colorNeedleEnd: "#3f48cc",
    colorBarProgress: "#327ac0",
    colorBar: "#f5f5f5",
    barStroke: 0,
    barWidth: 15,
    barBeginCircle: false
});
	

	gauge_PM1_out.value = PM1_Outdoor;
	gauge_PM1_out.draw();

	var gauge_PM2_5_in = new LinearGauge({
		renderTo: 'gauge_PM2_5_in',
		width: 320,
		height: 100,
		units: "",
		title: "PM2.5 indoor [ug/m3]",
		minValue: 0,
		maxValue: 160,
		majorTicks: [0,20,40,60,80,100,120,140,160],
		minorTicks: 5,
		strokeTicks: true,
		ticksWidth: 15,
		ticksWidthMinor: 7.5,
		highlights: [
        {
            "from": 0,
            "to": 40,
            "color": "rgba(29,239, 77, .9)"
        },
        {
            "from": 40,
            "to": 100,
            "color": "rgba(253, 126, 0, .9)"
        },
		{
            "from": 100,
            "to": 160,
            "color": "rgba(230, 0, 0, .9)"
        }
    ],
    colorMajorTicks: "#000000",
    colorMinorTicks: "#000000",
    colorTitle: "#000000",
    colorUnits: "#000000",
    colorNumbers: "#000000",
    colorPlate: "#ffffff",
    colorPlateEnd: "#ffffff",
    borderShadowWidth: 0,
    borders: false,
    borderRadius: 10,
    needleType: "arrow",
    needleWidth: 1,
	valueBox: true,
	animation: false,
    animationDuration: 100,
    animationRule: "linear",
    colorNeedle: "#3f48cc",
    colorNeedleEnd: "#3f48cc",
    colorBarProgress: "#327ac0",
    colorBar: "#f5f5f5",
    barStroke: 0,
    barWidth: 15,
    barBeginCircle: false
});
	

	gauge_PM2_5_in.value = PM2_5_Indoor;
	gauge_PM2_5_in.draw();


		var gauge_PM2_5_out = new LinearGauge({
		renderTo: 'gauge_PM2_5_out',
		width: 320,
		height: 100,
		units: "",
		title: "PM2.5 outdoor [ug/m3]",
		minValue: 0,
		maxValue: 160,
		majorTicks: [0,20,40,60,80,100,120,140,160],
		minorTicks: 5,
		strokeTicks: true,
		ticksWidth: 15,
		ticksWidthMinor: 7.5,
		highlights: [
        {
            "from": 0,
            "to": 40,
            "color": "rgba(29,239, 77, .9)"
        },
        {
            "from": 40,
            "to": 100,
            "color": "rgba(253, 126, 0, .9)"
        },
		{
            "from": 100,
            "to": 160,
            "color": "rgba(230, 0, 0, .9)"
        }
    ],
    colorMajorTicks: "#000000",
    colorMinorTicks: "#000000",
    colorTitle: "#000000",
    colorUnits: "#000000",
    colorNumbers: "#000000",
    colorPlate: "#ffffff",
    colorPlateEnd: "#ffffff",
    borderShadowWidth: 0,
    borders: false,
    borderRadius: 10,
    needleType: "arrow",
    needleWidth: 1,
	valueBox: true,
	animation: false,
    animationDuration: 100,
    animationRule: "linear",
    colorNeedle: "#3f48cc",
    colorNeedleEnd: "#3f48cc",
    colorBarProgress: "#327ac0",
    colorBar: "#f5f5f5",
    barStroke: 0,
    barWidth: 15,
    barBeginCircle: false
});
	

	gauge_PM2_5_out.value = PM2_5_Outdoor;
	gauge_PM2_5_out.draw();

	
	var gauge_PM10_in = new LinearGauge({
		renderTo: 'gauge_PM10_in',
		width: 320,
		height: 100,
		units: "",
		title: "PM10 indoor [ug/m3]",
		minValue: 0,
		maxValue: 160,
		majorTicks: [0,20,40,60,80,100,120,140,160],
		minorTicks: 5,
		strokeTicks: true,
		ticksWidth: 15,
		ticksWidthMinor: 7.5,
		highlights: [
        {
            "from": 0,
            "to": 40,
            "color": "rgba(29,239, 77, .9)"
        },
        {
            "from": 40,
            "to": 100,
            "color": "rgba(253, 126, 0, .9)"
        },
		{
            "from": 100,
            "to": 160,
            "color": "rgba(230, 0, 0, .9)"
        }
    ],
    colorMajorTicks: "#000000",
    colorMinorTicks: "#000000",
    colorTitle: "#000000",
    colorUnits: "#000000",
    colorNumbers: "#000000",
    colorPlate: "#ffffff",
    colorPlateEnd: "#ffffff",
    borderShadowWidth: 0,
    borders: false,
    borderRadius: 10,
    needleType: "arrow",
    needleWidth: 1,
	valueBox: true,
	animation: false,
    animationDuration: 100,
    animationRule: "linear",
    colorNeedle: "#3f48cc",
    colorNeedleEnd: "#3f48cc",
    colorBarProgress: "#327ac0",
    colorBar: "#f5f5f5",
    barStroke: 0,
    barWidth: 15,
    barBeginCircle: false
});
	

	gauge_PM10_in.value = PM10_Indoor;
	gauge_PM10_in.draw();


		var gauge_PM10_out = new LinearGauge({
		renderTo: 'gauge_PM10_out',
		width: 320,
		height: 100,
		units: "",
		title: "PM10 outdoor [ug/m3]",
		minValue: 0,
		maxValue: 160,
		majorTicks: [0,20,40,60,80,100,120,140,160],
		minorTicks: 5,
		strokeTicks: true,
		ticksWidth: 15,
		ticksWidthMinor: 7.5,
		highlights: [
        {
            "from": 0,
            "to": 40,
            "color": "rgba(29,239, 77, .9)"
        },
        {
            "from": 40,
            "to": 100,
            "color": "rgba(253, 126, 0, .9)"
        },
		{
            "from": 100,
            "to": 160,
            "color": "rgba(230, 0, 0, .9)"
        }
    ],
    colorMajorTicks: "#000000",
    colorMinorTicks: "#000000",
    colorTitle: "#000000",
    colorUnits: "#000000",
    colorNumbers: "#000000",
    colorPlate: "#ffffff",
    colorPlateEnd: "#ffffff",
    borderShadowWidth: 0,
    borders: false,
    borderRadius: 10,
    needleType: "arrow",
    needleWidth: 1,
	valueBox: true,
	animation: false,
    animationDuration: 100,
    animationRule: "linear",
    colorNeedle: "#3f48cc",
    colorNeedleEnd: "#3f48cc",
    colorBarProgress: "#327ac0",
    colorBar: "#f5f5f5",
    barStroke: 0,
    barWidth: 15,
    barBeginCircle: false
});
	

	gauge_PM10_out.value = PM10_Outdoor;
	gauge_PM10_out.draw();


// *************************************************		
		
		console.log(ajaxdata);
		
		data1_1.setValue(0,1,Temp_Outdoor);
		
		data1_2.setValue(0,1,Humid_Outdoor);
		data1_3.setValue(0,1,Press_Outdoor);
		
		data2.setValue(0,1,Current_L1);
		data2.setValue(1,1,Current_L2);
		data2.setValue(2,1,Current_L3);
		
				
		//data4_1.setValue(0,1,Temp_Room2);
		//data4_2.setValue(0,1,Humid_Room2);
		    
		chart1_1.draw(data1_1, options1_1);
		chart1_2.draw(data1_2, options1_2);
		chart1_3.draw(data1_3, options1_3);
		
		chart2.draw(data2, options2);
		
				
		//chart4_1.draw(data4_1, options4_1);
		//chart4_2.draw(data4_2, options4_2);
		
		if (Motion_Sensor1 == 1) 
		{
			$('div#led1_1').removeClass();
			$('div#led1_1').addClass('led-red');	
		}
		else if (Motion_Sensor1 == 0)
		{
			$('div#led1_1').removeClass();
			$('div#led1_1').addClass('led-green');	
		}
		
		if (Motion_Sensor2 == 1) 
		{
			$('div#led2_1').removeClass();
			$('div#led2_1').addClass('led-red');	
		}
		else if (Motion_Sensor2 == 0)
		{
			$('div#led2_1').removeClass();
			$('div#led2_1').addClass('led-green');	
		}
		
		if (Motion_Sensor3 == 1) 
		{
			$('div#led3_1').removeClass();
			$('div#led3_1').addClass('led-red');	
		}
		else if (Motion_Sensor3 == 0)
		{
			$('div#led3_1').removeClass();
			$('div#led3_1').addClass('led-green');	
		}
		
		if (Motion_Sensor4 == 1) 
		{
			$('div#led4_1').removeClass();
			$('div#led4_1').addClass('led-red');	
		}
		else if (Motion_Sensor4 == 0)
		{
			$('div#led4_1').removeClass();
			$('div#led4_1').addClass('led-green');	
		}
		
      }
       

function status_update() {
               var jqxhr = $.getJSON('data.php?' + 'random=' + Math.random(), function() {
              })
              .fail(function() {
              })
              .done(function(ajaxdata) {
              test(ajaxdata);
              });
      }
       
// cyclically update values for analog gauges
var refreshId = setInterval('status_update()', 200);
$.ajaxSetup({ cache: false });

</script>
	

	
<script type="text/javascript" src="jquery.js"></script>
<script>

$(document).ready(function(){

// *********************************************
// ************ Checkboxes ROOM 1 **************
// *********************************************

$('#checkbox1_1').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox1_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room1.php', { value:"checkbox1_1_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
											//$.post('cb_CLEAR_Val.php', { value:"checkbox1_1_OFF" } );
										    $.post('../home_automation_data/cb_set_data_room1.php', { value:"checkbox1_1_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });


$('#checkbox1_2').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox1_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room1.php', { value:"checkbox1_2_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
											//$.post('cb_CLEAR_Val.php', { value:"checkbox1_1_OFF" } );
										    $.post('../home_automation_data/cb_set_data_room1.php', { value:"checkbox1_2_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
$('#checkbox1_3').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox1_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room1.php', { value:"checkbox1_3_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
											//$.post('cb_CLEAR_Val.php', { value:"checkbox1_1_OFF" } );
										    $.post('../home_automation_data/cb_set_data_room1.php', { value:"checkbox1_3_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										  									   
// *********************************************
// ************ Checkboxes ROOM 2 **************
// *********************************************
$('#checkbox2_1').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox2_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room2.php', { value:"checkbox2_1_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
										    //$.post('cb_SET_Val.php', { value:"checkbox2_1_OFF" } );
											$.post('../home_automation_data/cb_set_data_room2.php', { value:"checkbox2_1_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
$('#checkbox2_2').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox2_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room2.php', { value:"checkbox2_2_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
										    //$.post('cb_SET_Val.php', { value:"checkbox2_1_OFF" } );
											$.post('../home_automation_data/cb_set_data_room2.php', { value:"checkbox2_2_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
$('#checkbox2_3').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox2_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room2.php', { value:"checkbox2_3_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
										    //$.post('cb_SET_Val.php', { value:"checkbox2_1_OFF" } );
											$.post('../home_automation_data/cb_set_data_room2.php', { value:"checkbox2_3_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
										   
function handle_cb_Click(cb){
	
	
	if(cb.checked) {
					//var value = "test";
					//alert ("checked=" + cb.checked);		//it works!
												
	 
					var cbID=cb.id;
					//alert(cb.id);				//it works
					$.post('cb_SET_Val.php', { value:cbID } );
	 /*$.AJAX({
				type: 'POST',
				url: 'checkbox_test.php'
			}); */ 
	}else{
				//alert ("UN_checked=" + cb.checked);					//it works!
				var cbID=cb.id;
				//alert(cb.id);											//it works
				$.post('cb_CLEAR_Val.php', { value: cbID } );
	 
	 //$.post('checkbox_test2.php', { value:"checkbox1_ON" } );
	 /*$.AJAX({
				type: 'POST',
				url: 'checkbox_test2.php'
			}); */ 
  }
}

});

</script>



</body>
</html>
