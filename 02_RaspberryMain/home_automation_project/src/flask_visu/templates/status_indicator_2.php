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

<script type="text/javascript">
function updateSlider(slideAmount) {
}

</script>

</head>

<body>

<h1 style="font-family: courier;" align="center">HOME Automation System 2</h1>


<!-- ****************************************** -->
<!-- ***************  ROOM 1 ****************** -->
<!-- ****************************************** -->

<!-- show analog temperature gauge Room 1 ( living room ) -->
<div style="position:absolute; left:50px; top: 80px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 120px;" >ROOM 1/Living</p>
	<div id="gauge1_1" style="width: 250px; height: 50px;"></div>
</div> 

<!-- show analog humidity gauge Room 1 ( living room ) -->
<div style="position:absolute; left:190px; top: 100px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 60px;" > </p>
	<div id="gauge1_2" style="width: 250px; height: 50px;"></div>
</div>

<!-- button for Line Chart for Living Room-->
<div style="position:absolute; left:170px; top: 230px; font-family:courier" >
	<button onClick="window.open('./LineCharts_Room1.php','LineChart Room1','width=600,height=700,left=250,top=200,toolbar=0,status=0')"  > Charts </button>
</div>  


<div>
	<!--<img id="myImage" src="pic_bulboff.gif" width="100" height="180">-->
</div>


<!--LED indicators -->
<div id="container-vertical" class="container" style="position:absolute; left: 170px; top:300px">
  <div class="led-box"  >
    <div id="led1_1" class="led-green"  ></div>
    <p style="position:relative; left: 26px; top:-20px">Motion detection</p>
  </div>
  
  <div class="led-box" >
    <div id="led1_2" class="led-green"  ></div>
    <p>Alarm 1</p>
  </div>
  
  <div class="led-box" >
    <div id="led1_3" class="led-green"  ></div>
    <p>Alarm 2</p>
  </div>
  
  <div class="led-box"  >
    <div id="led1_4" class="led-blue"  ></div>
    <p>Alarm 3</p>
  </div>

<!--
  <div class="led-box" >
    <div id="led1_5" class="led-yellow"  ></div>
    <p>Alarm 4</p>
  </div>
  
  <div class="led-box" >
    <div id="led1_6" class="led-yellow"  ></div>
    <p>Alarm 5</p>
  </div>
-->

</div>

<!--big black ON/OFF switch with lever -->
<!--font-size defines the size of the switch -->
<span class="switch demo5" style="position: absolute; top:260px; left:70px; font-size: 8px;">
	<span class="switch-border1">
		<span class="switch-border2">
			<input id="checkbox1_1" type="checkbox" name="" onclick=""
																	<?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room1/checkbox1_1");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
	
																	?> 
			>
			<label for="checkbox1_1"></label>
			<span class="switch-top"></span>
			<span class="switch-shadow"></span>
			<span class="switch-handle"></span>
			<span class="switch-handle-left"></span>
			<span class="switch-handle-right"></span>
			<span class="switch-handle-top"></span>
			<span class="switch-handle-bottom"></span>
			<span class="switch-handle-base"></span>
			<span class="switch-led switch-led-green">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
			<span class="switch-led switch-led-red">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
		</span>
	</span>
</span>

<!-- round switch 1 = Checkbox 1_2 -->
<div style="position:absolute; left:90px; top: 520px; font-family:courier;" class="przycisk demo4">
					<input id="checkbox1_2" type="checkbox" name="" onclick="" <?php
																				// php reads status of the checkbox variable and set according to it the property "checked"
																				$button_get_status = file_get_contents("/var/www/html/home_automation_data/room1/checkbox1_2");
																				if ($button_get_status == "1" ) {
																												echo "checked='checked'";
																												} 
																				?> 
					
					>
					<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch1_2</b>
</div>

<!-- round switch 2 = Checkbox 1_3-->
<div style="position:absolute; left:190px; top: 520px; font-family:courier;" class="przycisk demo4">
					<input id="checkbox1_3" type="checkbox" name="" onclick=""  <?php
																				// php reads status of the checkbox variable and set according to it the property "checked"
																				$button_get_status = file_get_contents("/var/www/html/home_automation_data/room1/checkbox1_3");
																				if ($button_get_status == "1" ) {
																												echo "checked='checked'";
																												} 
																				?> 
					
					>
					<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch1_3</b>
</div>

<!-- slider  Heating -->
<div id="slider" style="position:absolute; left:80px; top:700px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider1_1" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room1/heating_1");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?> 
  
  
  >
  <p style="font-family:courier">Value=: <span id="mySlider1_1_Value"></span></p>
  <p style="position:relative; left:50px; top:-65px; font-family:courier; font-size:18px;" >Heating</p>
</div>

<!-- slider Light intense -->
<div id="slider" style="position:absolute; left:80px; top:800px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider1_2" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room1/light_intense_1");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?> 
  
  >
  <p style="font-family:courier">Value=: <span id="mySlider1_2_Value"></span></p>
  <p style="position:relative; left:25px; top:-65px; font-family:courier; font-size:18px;" >Light intense</p>
</div>


<!-- ****************************************** -->
<!-- ***************  ROOM 2 ****************** -->
<!-- ****************************************** -->

<!-- show analog temperature gauge Room 2 (bedroom)  -->
<div style="position:absolute; left:350px; top: 80px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 120px;" >ROOM 2/Bed</p>
	<div id="gauge2_1" style="width: 300px; height: 50px;"></div>
</div> 

<!-- show analog humidity gauge Room 2 (bedroom) -->
<div style="position:absolute; left:490px; top: 100px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 60px;" > </p>
	<div id="gauge2_2" style="width: 300px; height: 50px;"></div>
</div> 

<!-- button Line Chart for Room 2 / Bed Room-->
<div style="position:absolute; left:470px; top: 230px; font-family:courier" >
	<button onClick="window.open('./LineCharts_Room2.php','LineChart Room2','width=600,height=400,left=250,top=200,toolbar=0,status=0')"  > Charts </button>
</div> 


<!--LED indicators -->
<div id="container-vertical" class="container" style="position:absolute; left: 470px; top:300px">
  <div class="led-box"  >
    <div id="led2_1" class="led-green"  ></div>
    <p style="position:relative; left: 26px; top:-20px">Motion detection</p>
  </div>
  
  <div class="led-box" >
    <div id="led2_2" class="led-green"  ></div>
    <p>Alarm 1</p>
  </div>
  
  <div class="led-box" >
    <div id="led2_3" class="led-green"  ></div>
    <p>Alarm 2</p>
  </div>
  
  <div class="led-box"  >
    <div id="led2_4" class="led-blue"  ></div>
    <p>Alarm 3</p>
  </div>

<!--
  <div class="led-box" >
    <div id="led2_5" class="led-yellow"  ></div>
    <p>Alarm 4</p>
  </div>
  
  <div class="led-box" >
    <div id="led2_6" class="led-yellow"  ></div>
    <p>Alarm 5</p>
  </div>
 --> 
 
</div>


<!--big black ON/OFF switch with lever -->
<!--font-size defines the size of the switch -->
<span class="switch demo5" style="position: absolute; top:260px; left:370px; font-size: 8px;">
	<span class="switch-border1">
		<span class="switch-border2">
			<input id="checkbox2_1" type="checkbox" name="" onclick=""
																	<?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room2/checkbox2_1");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
	
																	?> 
			>
			<label for="checkbox2_1"></label>
			<span class="switch-top"></span>
			<span class="switch-shadow"></span>
			<span class="switch-handle"></span>
			<span class="switch-handle-left"></span>
			<span class="switch-handle-right"></span>
			<span class="switch-handle-top"></span>
			<span class="switch-handle-bottom"></span>
			<span class="switch-handle-base"></span>
			<span class="switch-led switch-led-green">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
			<span class="switch-led switch-led-red">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
		</span>
	</span>
</span>

<!-- round switch 1 = Checkbox 2_2 -->
<div style="position:absolute; left:390px; top: 520px; font-family:courier;" class="przycisk demo4">
						<input id="checkbox2_2" type="checkbox"  <?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room2/checkbox2_2");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
																	?> 
						
						>
						<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch2_2</b>
</div>

<!-- round switch 2 = Checkbox 2_3-->
<div style="position:absolute; left:490px; top: 520px; font-family:courier;" class="przycisk demo4">
						<input id="checkbox2_3" type="checkbox"  <?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room2/checkbox2_3");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
																	?> 
						
						>
						<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch2_3</b>
</div>


<!-- slider  Heating -->
<div id="slider" style="position:absolute; left:380px; top:700px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider2_1" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room2/heating_2");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?>
  
  >
  <p style="font-family:courier; font-size:16px">Value=: <span id="mySlider2_1_Value"></span></p>
  <p style="position:relative; left:50px; top:-65px; font-family:courier; font-size:18px;" >Heating</p>
</div>


<!-- slider  Light intense  -->
<div id="slider" style="position:absolute; left:380px; top:800px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider2_2" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room2/light_intense_2");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?>
  
  >
  <p style="font-family:courier">Value=: <span id="mySlider2_2_Value"></span></p>
  <p style="position:relative; left:25px; top:-65px; font-family:courier; font-size:18px;" >Light intense</p>
</div>


<!-- ****************************************** -->
<!-- ***************  ROOM 3 ****************** -->
<!-- ****************************************** -->

<!-- show analog temperature gauge Room 3 ( kitchen ) -->
<div style="position:absolute; left:680px; top: 80px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 80px;" >ROOM 3/Kitchen</p>
	<div id="gauge3_1" style="width: 250px; height: 50px;"></div>
</div> 

<!-- show analog humidity gauge Room 3 ( kitchen ) -->
<div style="position:absolute; left:820px; top: 100px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 60px;" > </p>
	<div id="gauge3_2" style="width: 250px; height: 50px;"></div>
</div> 

<!--Navigation button Line Chart for room3 (kitchen) -->
<div style="position:absolute; left:800px; top: 230px; font-family:courier" >
	<button onClick="window.open('./LineCharts_Room3.php','LineChart Room3','width=580,height=640,left=50,top=250,toolbar=0,status=0')"  > Charts </button>
</div> 


<div>
	<!--<img id="myImage" src="pic_bulboff.gif" width="100" height="180">-->
</div>


<!--LED indicators -->
<div id="container-vertical" class="container" style="position:absolute; left: 820px; top:300px">
  <div class="led-box"  >
    <div id="led3_1" class="led-green"  ></div>
    <p style="position:relative; left: 26px; top:-20px">Motion detection</p>
  </div>
  
  <div class="led-box" >
    <div id="led3_2" class="led-green"  ></div>
    <p>Smoke alarm</p>
  </div>
  
  <div class="led-box" >
    <div id="led3_3" class="led-green"  ></div>
    <p>Alarm 2</p>
  </div>
  
  <div class="led-box"  >
    <div id="led3_4" class="led-blue"  ></div>
    <p>Alarm 3</p>
  </div>

<!--
  <div class="led-box" >
    <div id="led3_5" class="led-yellow"  ></div>
    <p>Alarm 4</p>
  </div>
  
  <div class="led-box" >
    <div id="led3_6" class="led-yellow"  ></div>
    <p>Alarm 5</p>
  </div>
-->  
</div>

<!--big black ON/OFF switch with lever -->
<!--font-size defines the size of the switch -->
<span class="switch demo5" style="position: absolute; top:260px; left:720px; font-size: 8px;">
	<span class="switch-border1">
		<span class="switch-border2">
			<input id="checkbox3_1" type="checkbox" name="" onclick=""
																	<?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room3/checkbox3_1");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
	
																	?> 
			>
			<label for="checkbox3_1"></label>
			<span class="switch-top"></span>
			<span class="switch-shadow"></span>
			<span class="switch-handle"></span>
			<span class="switch-handle-left"></span>
			<span class="switch-handle-right"></span>
			<span class="switch-handle-top"></span>
			<span class="switch-handle-bottom"></span>
			<span class="switch-handle-base"></span>
			<span class="switch-led switch-led-green">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
			<span class="switch-led switch-led-red">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
		</span>
	</span>
</span>

<!-- round switch 1 = Checkbox 3_2 -->
<div style="position:absolute; left:730px; top: 520px; font-family:courier;" class="przycisk demo4">
					<input id="checkbox3_2" type="checkbox" name="" onclick="" <?php
																				// php reads status of the checkbox variable and set according to it the property "checked"
																				$button_get_status = file_get_contents("/var/www/html/home_automation_data/room3/checkbox3_2");
																				if ($button_get_status == "1" ) {
																												echo "checked='checked'";
																												} 
																				?> 
					
					>
					<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch3_2</b>
</div>

<!-- round switch 2 = Checkbox 3_3-->
<div style="position:absolute; left:830px; top: 520px; font-family:courier;" class="przycisk demo4">
					<input id="checkbox3_3" type="checkbox" name="" onclick=""  <?php
																				// php reads status of the checkbox variable and set according to it the property "checked"
																				$button_get_status = file_get_contents("/var/www/html/home_automation_data/room3/checkbox3_3");
																				if ($button_get_status == "1" ) {
																												echo "checked='checked'";
																												} 
																				?> 
					
					>
					<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch3_3</b>
</div>

<!-- slider  Heating -->
<div id="slider" style="position:absolute; left:730px; top:700px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider3_1" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room3/heating_3");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?> 
  
  
  >
  <p style="font-family:courier">Value=: <span id="mySlider3_1_Value"></span></p>
  <p style="position:relative; left:50px; top:-65px; font-family:courier; font-size:18px;" >Heating</p>
</div>

<!-- slider Light intense -->
<div id="slider" style="position:absolute; left:730px; top:800px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider3_2" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room3/light_intense_3");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?> 
  
  >
  <p style="font-family:courier">Value=: <span id="mySlider3_2_Value"></span></p>
  <p style="position:relative; left:25px; top:-65px; font-family:courier; font-size:18px;" >Light intense</p>
</div>


<!-- ****************************************** -->
<!-- ***************  ROOM 4 ****************** -->
<!-- ****************************************** -->

<!-- show analog temperature gauge Room 4 ( bathroom ) -->
<div style="position:absolute; left:980px; top: 80px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 90px;" >ROOM 4/Bath</p>
	<div id="gauge4_1" style="width: 300px; height: 50px;"></div>
</div>

<!-- show analog humidity gauge Room 4 ( bathroom ) -->
<div style="position:absolute; left:1120px; top: 100px; font-family:courier">
	<p class="a" style="position:relative;width:200px; left: 60px;" > </p>
	<div id="gauge4_2" style="width: 300px; height: 50px;"></div>
</div>

<!--Navigation button Line Chart for room4 (bath) -->
<div style="position:absolute; left:1100px; top: 230px; font-family:courier" >
	<button onClick="window.open('./LineCharts_Room4.php','LineChart Room4','width=550,height=400,left=50,top=200,toolbar=0,status=0')"  > Charts </button>
</div> 
 

<!--LED indicators -->
<div id="container-vertical" class="container" style="position:absolute; left: 1100px; top:300px">
  <div class="led-box"  >
    <div id="led4_1" class="led-green"  ></div>
    <p style="position:relative; left: 26px; top:-20px">Motion detection</p>
  </div>
  
  <div class="led-box" >
    <div id="led4_2" class="led-green"  ></div>
    <p>Alarm 1</p>
  </div>
  
  <div class="led-box" >
    <div id="led4_3" class="led-green"  ></div>
    <p>Alarm 2</p>
  </div>
  
  <div class="led-box"  >
    <div id="led4_4" class="led-blue"  ></div>
    <p>Alarm 3</p>
  </div>

<!--
  <div class="led-box" >
    <div id="led4_5" class="led-yellow"  ></div>
    <p>Alarm 4</p>
  </div>
  
  <div class="led-box" >
    <div id="led4_6" class="led-yellow"  ></div>
    <p>Alarm 5</p>
  </div>
-->  
</div>


<!--big black ON/OFF switch with lever -->
<!--font-size defines the size of the switch -->
<span class="switch demo5" style="position: absolute; top:260px; left:1010px; font-size: 8px;">
	<span class="switch-border1">
		<span class="switch-border2">
			<input id="checkbox4_1" type="checkbox" name="" onclick=""
																	<?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room4/checkbox4_1");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
	
																	?> 
			>
			<label for="checkbox4_1"></label>
			<span class="switch-top"></span>
			<span class="switch-shadow"></span>
			<span class="switch-handle"></span>
			<span class="switch-handle-left"></span>
			<span class="switch-handle-right"></span>
			<span class="switch-handle-top"></span>
			<span class="switch-handle-bottom"></span>
			<span class="switch-handle-base"></span>
			<span class="switch-led switch-led-green">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
			<span class="switch-led switch-led-red">
				<span class="switch-led-border">
					<span class="switch-led-light">
						<span class="switch-led-glow"></span>
					</span>
				</span>
			</span>
		</span>
	</span>
</span>

<!-- round switch 1 = Checkbox 4_2 -->
<div style="position:absolute; left:1030px; top: 520px; font-family:courier;" class="przycisk demo4">
						<input id="checkbox4_2" type="checkbox"  <?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room4/checkbox4_2");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
																	?> 
						
						>
						<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch4_2</b>
</div>

<!-- round switch 2 = Checkbox 4_3-->
<div style="position:absolute; left:1120px; top: 520px; font-family:courier;" class="przycisk demo4">
						<input id="checkbox4_3" type="checkbox"  <?php
																	// php reads status of the checkbox variable and set according to it the property "checked"
																	$button_get_status = file_get_contents("/var/www/html/home_automation_data/room4/checkbox4_3");
																		if ($button_get_status == "1" ) {
																										echo "checked='checked'";
																										} 
																	?> 
						
						>
						<label><i class='icon-off'></i></label>
					<b style="position:relative; top:-75px" >switch4_3</b>
</div>


<!-- slider  Heating -->
<div id="slider" style="position:absolute; left:1020px; top:700px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider4_1" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room4/heating_4");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?>
  
  >
  <p style="font-family:courier; font-size:16px">Value=: <span id="mySlider4_1_Value"></span></p>
  <p style="position:relative; left:50px; top:-65px; font-family:courier; font-size:18px;" >Heating</p>
</div>


<!-- slider  Light intense  -->
<div id="slider" style="position:absolute; left:1020px; top:800px; width:200px">
  <input type="range" min="1" max="100" class="slider" id="mySlider4_2" <?php
																				// php reads status of the slider value from file and set according to it its property "value"
																				$slider_get_value = file_get_contents("/var/www/html/home_automation_data/room4/light_intense_4");
																				if ($slider_get_value > 0 ) {
																												echo "value='$slider_get_value'";
																												} 
																				?>
  
  >
  <p style="font-family:courier">Value=: <span id="mySlider4_2_Value"></span></p>
  <p style="position:relative; left:25px; top:-65px; font-family:courier; font-size:18px;" >Light intense</p>
</div>


<!--Navigation button 1 -->
<div style="position:absolute; left:1500px; top: 700px; font-family:courier; width: 90px;" >
	<button class="w3-button w3-cyan" onclick="window.location.href='status_indicator_1.php';"  > Main Home Automation </button>
</div> 

<!--Navigation button 2 -->
<div style="position:absolute; left:1500px; top: 750px; font-family:courier; width: 90px;" >
	<button class="w3-button w3-cyan" onclick="window.location.href='status_indicator_3.php';"  >... Camera ... </button>
</div> 

<script>

// ******************** ROOM 1 slider *****************************
var slider1_1 = document.getElementById("mySlider1_1");
var output1_1 = document.getElementById("mySlider1_1_Value");

var slider1_2 = document.getElementById("mySlider1_2");
var output1_2 = document.getElementById("mySlider1_2_Value");

// ******************** ROOM 2 slider *****************************
var slider2_1 = document.getElementById("mySlider2_1");
var output2_1 = document.getElementById("mySlider2_1_Value");

var slider2_2 = document.getElementById("mySlider2_2");
var output2_2 = document.getElementById("mySlider2_2_Value");

// ******************** ROOM 1 slider *****************************
output1_1.innerHTML = slider1_1.value;
output1_2.innerHTML = slider1_2.value;

output2_1.innerHTML = slider2_1.value;
output2_2.innerHTML = slider2_2.value;

slider1_1.oninput = function() {
  output1_1.innerHTML = this.value;
  $.post('../home_automation_data/slider1_1_set_data.php', { value: slider1_1.value } );
}

slider1_2.oninput = function() {
  output1_2.innerHTML = this.value;
  //if (this.value > 90) { window.alert(" room 1 slider");}
  $.post('../home_automation_data/slider1_2_set_data.php', { value: slider1_2.value } );
}

// ******************** ROOM 2 slider *****************************
slider2_1.oninput = function() {
  output2_1.innerHTML = this.value;
  $.post('../home_automation_data/slider2_1_set_data.php', { value: slider2_1.value } );
}

slider2_2.oninput = function() {
  output2_2.innerHTML = this.value;
  //if (this.value > 90) { window.alert(" room 2 slider");}
  $.post('../home_automation_data/slider2_2_set_data.php', { value: slider2_2.value } );
}


// ******************** ROOM 3 slider *****************************
var slider3_1 = document.getElementById("mySlider3_1");
var output3_1 = document.getElementById("mySlider3_1_Value");

var slider3_2 = document.getElementById("mySlider3_2");
var output3_2 = document.getElementById("mySlider3_2_Value");

// ******************** ROOM 4 slider *****************************
var slider4_1 = document.getElementById("mySlider4_1");
var output4_1 = document.getElementById("mySlider4_1_Value");

var slider4_2 = document.getElementById("mySlider4_2");
var output4_2 = document.getElementById("mySlider4_2_Value");

// ******************** ROOM 3 slider *****************************
output3_1.innerHTML = slider3_1.value;
output3_2.innerHTML = slider3_2.value;

slider3_1.oninput = function() {
  output3_1.innerHTML = this.value;
  $.post('../home_automation_data/slider3_1_set_data.php', { value: slider3_1.value } );
}

slider3_2.oninput = function() {
  output3_2.innerHTML = this.value;
  //if (this.value > 90) { window.alert(" room 1 slider");}
  $.post('../home_automation_data/slider3_2_set_data.php', { value: slider3_2.value } );
}

// ******************** ROOM 4 slider *****************************
output4_1.innerHTML = slider4_1.value;
output4_2.innerHTML = slider4_2.value;

slider4_1.oninput = function() {
  output4_1.innerHTML = this.value;
  $.post('../home_automation_data/slider4_1_set_data.php', { value: slider4_1.value } );
}

slider4_2.oninput = function() {
  output4_2.innerHTML = this.value;
  //if (this.value > 90) { window.alert(" room 2 slider");}
  $.post('../home_automation_data/slider4_2_set_data.php', { value: slider4_2.value } );
}

  
</script>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script src="jquery.min.js"></script>
<script type="text/javascript">

	  // draw gauge visualizations
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawVisualization);
	 
      	  
	  
	  $(document).ready(function() {
		  
		});
		  
		  
		// draw gauges
		function drawVisualization() {
		
		// room 1 - temperature gauge
		data1_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options1_1 = {
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
		
		chart1_1 = new google.visualization.Gauge(document.getElementById('gauge1_1'));
 
		// room 1 - humidity gauge
		data1_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid', 0],
        ]);
 
        options1_2 = {
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
		
		chart1_2 = new google.visualization.Gauge(document.getElementById('gauge1_2'));
		
		// room 2 - temperature gauge
		data2_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options2_1 = {
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
		
		chart2_1 = new google.visualization.Gauge(document.getElementById('gauge2_1'));
 
		// room 2 - humidity gauge
		data2_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid', 0],
        ]);
 
        options2_2 = {
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
		
		chart2_2 = new google.visualization.Gauge(document.getElementById('gauge2_2'));
		
		
		// room 3 - temperature gauge
        data3_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options3_1 = {
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
		
		chart3_1 = new google.visualization.Gauge(document.getElementById('gauge3_1'));
		
		// room 3 - humidity gauge
        data3_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid.', 0],
        ]);
 
        options3_2 = {
          width: 300, height: 150,
          max:100, min:0,
          animation:{duration: 400},
	      greenColor:'#08E3E8',
          greenFrom:0, greenTo:100,
          minorTicks: 5,
          majorTicks: [0,10,20,30,40,50,60,70,80,90,100]
        };
		
		chart3_2 = new google.visualization.Gauge(document.getElementById('gauge3_2'));
		
		
		// room 4 - temperature gauge
        data4_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options4_1 = {
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
		
		chart4_1 = new google.visualization.Gauge(document.getElementById('gauge4_1'));
		
		
		// room 4 - humidity gauge
        data4_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid.', 0],
        ]);
 
        options4_2 = {
          width: 300, height: 150,
          max:100, min:0,
          animation:{duration: 400},
	      greenColor:'#08E3E8',
          greenFrom:0, greenTo:100,
          minorTicks: 5,
          majorTicks: [0,10,20,30,40,50,60,70,80,90,100]
        };	
		
		chart4_2 = new google.visualization.Gauge(document.getElementById('gauge4_2'));
		
        chart1_1.draw(data1_1, options1_1);
		chart1_2.draw(data1_2, options1_2);
		
		chart2_1.draw(data2_1, options2_1);
		chart2_2.draw(data2_2, options2_2);
		
		chart3_1.draw(data3_1, options3_1);
		chart3_2.draw(data3_2, options3_2);
		
		chart4_1.draw(data4_1, options4_1);
		chart4_2.draw(data4_2, options4_2);
									}
		
		
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
		
		var Motion_Sensor1=ajaxdata.MotionSensor1_AJAX; 
		var Motion_Sensor2=ajaxdata.MotionSensor2_AJAX;
		var Motion_Sensor3=ajaxdata.MotionSensor3_AJAX;
		var Motion_Sensor4=ajaxdata.MotionSensor4_AJAX;
		var Motion_Sensor5=ajaxdata.MotionSensor5_AJAX;
		
		var Smoke_Sensor3=ajaxdata.SmokeSensor3_AJAX;
		
		console.log(ajaxdata);
		
		// settings for temp/humid gauge
		data1_1.setValue(0,1,Temp_Room1);
		data1_2.setValue(0,1,Humid_Room1);
		
		data2_1.setValue(0,1,Temp_Room2);
		data2_2.setValue(0,1,Humid_Room2);
		
		data3_1.setValue(0,1,Temp_Room3);
		data3_2.setValue(0,1,Humid_Room3);
		
		data4_1.setValue(0,1,Temp_Room4);
		data4_2.setValue(0,1,Humid_Room4);
		
		//display gauge for temp/humid
		chart1_1.draw(data1_1, options1_1);
		chart1_2.draw(data1_2, options1_2);
		
		chart2_1.draw(data2_1, options2_1);
		chart2_2.draw(data2_2, options2_2);
		    
		chart3_1.draw(data3_1, options3_1);
		chart3_2.draw(data3_2, options3_2);
		
		chart4_1.draw(data4_1, options4_1);
		chart4_2.draw(data4_2, options4_2);
		
		
		// room 1 - temperature gauge settings
		data1_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options1_1 = {
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
		
		chart1_1 = new google.visualization.Gauge(document.getElementById('gauge1_1'));
 
		// room 1 - humidity gauge settings
		data1_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid', 0],
        ]);
 
        options1_2 = {
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
		
		chart1_2 = new google.visualization.Gauge(document.getElementById('gauge1_2'));
		
		// room 2 - temperature gauge settings
		data2_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options2_1 = {
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
		
		chart2_1 = new google.visualization.Gauge(document.getElementById('gauge2_1'));
 
		// room 2 - humidity gauge settings
		data2_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid', 0],
        ]);
 
        options2_2 = {
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
		
		chart2_2 = new google.visualization.Gauge(document.getElementById('gauge2_2'));
		
		// room 3 - temperature gauge settings
        data3_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options3_1 = {
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
		
		// room 3 - humidity gauge settings
        data3_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid.', 0],
        ]);
 
        options3_2 = {
          width: 300, height: 150,
          max:100, min:0,
          animation:{duration: 400},
	      greenColor:'#08E3E8',
          greenFrom:0, greenTo:100,
          minorTicks: 5,
          majorTicks: [0,10,20,30,40,50,60,70,80,90,100]
        };
		
		// room 4 - temperature gauge settings
        data4_1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp', 0],
        ]);
 
        options4_1 = {
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
		
		// room 4 - humidity gauge settings
        data4_2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humid.', 0],
        ]);
 
        options4_2 = {
          width: 300, height: 150,
          max:100, min:0,
          animation:{duration: 400},
	      greenColor:'#08E3E8',
          greenFrom:0, greenTo:100,
          minorTicks: 5,
          majorTicks: [0,10,20,30,40,50,60,70,80,90,100]
        };	
		
		chart1_1 = new google.visualization.Gauge(document.getElementById('gauge1_1'));
		chart1_2 = new google.visualization.Gauge(document.getElementById('gauge1_2'));
		chart2_1 = new google.visualization.Gauge(document.getElementById('gauge2_1'));
		chart2_2 = new google.visualization.Gauge(document.getElementById('gauge2_2'));
		chart3_1 = new google.visualization.Gauge(document.getElementById('gauge3_1'));
		chart3_2 = new google.visualization.Gauge(document.getElementById('gauge3_2'));
		chart4_1 = new google.visualization.Gauge(document.getElementById('gauge4_1'));
		chart4_2 = new google.visualization.Gauge(document.getElementById('gauge4_2'));
		
		
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
		
		if (Smoke_Sensor3 == 1) 
		{
			$('div#led3_2').removeClass();
			$('div#led3_2').addClass('led-red');	
		}
		else if (Smoke_Sensor3 == 0)
		{
			$('div#led3_2').removeClass();
			$('div#led3_2').addClass('led-green');	
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
       
      var refreshId = setInterval('status_update()', 300);
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



// *********************************************
// ************ Checkboxes ROOM 3 **************
// *********************************************

$('#checkbox3_1').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox1_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room3.php', { value:"checkbox3_1_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
											//$.post('cb_CLEAR_Val.php', { value:"checkbox1_1_OFF" } );
										    $.post('../home_automation_data/cb_set_data_room3.php', { value:"checkbox3_1_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });


$('#checkbox3_2').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox1_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room3.php', { value:"checkbox3_2_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
											//$.post('cb_CLEAR_Val.php', { value:"checkbox1_1_OFF" } );
										    $.post('../home_automation_data/cb_set_data_room3.php', { value:"checkbox3_2_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
$('#checkbox3_3').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox1_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room3.php', { value:"checkbox3_3_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
											//$.post('cb_CLEAR_Val.php', { value:"checkbox1_1_OFF" } );
										    $.post('../home_automation_data/cb_set_data_room3.php', { value:"checkbox3_3_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										  									   
// *********************************************
// ************ Checkboxes ROOM 4 **************
// *********************************************
$('#checkbox4_1').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox2_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room4.php', { value:"checkbox4_1_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
										    //$.post('cb_SET_Val.php', { value:"checkbox2_1_OFF" } );
											$.post('../home_automation_data/cb_set_data_room4.php', { value:"checkbox4_1_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
$('#checkbox4_2').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox2_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room4.php', { value:"checkbox4_2_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
										    //$.post('cb_SET_Val.php', { value:"checkbox2_1_OFF" } );
											$.post('../home_automation_data/cb_set_data_room4.php', { value:"checkbox4_2_OFF" } );
											//alert (" ++++  checkbox unchecked");
											//alert(cbID);
										   }
										   });
										   
$('#checkbox4_3').on('change', function() {
		if ($(this).is(':checked')) {		
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_SET_Val.php', { value:cbID } );
											//$.post('cb_SET_Val.php', { value:"checkbox2_1_ON" } );
											$.post('../home_automation_data/cb_set_data_room4.php', { value:"checkbox4_3_ON" } );
											//alert (" ---- checkbox checked");
											//alert(cbID);
											
									  
									} else {
											var cbID=$(this).attr('id');
											//var value = $(this).val();
											//$.post('cb_CLEAR_Val.php', { value:cbID } );
										    //$.post('cb_SET_Val.php', { value:"checkbox2_1_OFF" } );
											$.post('../home_automation_data/cb_set_data_room4.php', { value:"checkbox4_3_OFF" } );
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
