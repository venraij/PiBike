<!DOCTYPE html>
<html>
<head>
<title>Pi - Bike</title>
<link rel="stylesheet" href="stylesheet.css">
</head>
<body>
    <style>
       /* Set the size of the div element that contains the map */
      #map {
        height: 300px;  /* The height is 200 pixels */
        width: 75%;  /* The width is the width of the web page */
       }
    </style>
<header>
<p>Fietslocatie</p>
</header>
<section>
<nav>
<ul style="list-style-type:none;">
    <li><a href="index.html">Hoofdpagina</a></li>
    <li><a href="gps.php">Fietslocatie</a></li>
    <li><a href="valdetectie.html">Val detectie</a></li>
    <li><a href="diefstal.html">Diefstal alarm</a></li>
    <li><a href="parkeren.html">Parkeer assistentie</a></li>
</ul>
</nav>
<article>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script> 
    <center><h3>Huidige Fietslocatie</h3>
    <div class="mypanel"></div>
    <!--The div element for the map -->
    <div id="map"></div>
	     
    	?php
	$servername = "localhost";
	$username = "nickvraaij_pibike";
	$password = "pibike";
	$dbname = "nickvraaij_pibike";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}

        $link = mysqli_connect("localhost", "nickvraaij_pibike", "pibike", "nickvraaij_pibike");

	$lon = mysqli_query($link, "SELECT waarde FROM meting WHERE sensor_id = 2 ORDER BY id DESC LIMIT 1");
	
	$lat = mysqli_query($link, "SELECT waarde FROM meting WHERE sensor_id = 1 ORDER BY id DESC LIMIT 1");

        $lonresult = mysqli_fetch_assoc($lon);
        $latresult = mysqli_fetch_assoc($lat);

	$conn->close();
	?>   
	    
    <script>


// Initialize and add the map
function initMap() {
  // The location of Uluru
  var uluru = {lat: <?php echo ($latresult['waarde']) ?>, lng: <?php echo ($lonresult['waarde']) ?>};
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 4, center: uluru});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: uluru, map: map});
}
    </script>
    <!--Load the API from the specified URL
    * The async attribute allows the browser to render the page while the API loads
    * The key parameter will contain your own API key (which is not needed for this tutorial)
    * The callback parameter executes the initMap() function
    -->
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBnejzs-LTCWKvYc9YSAB_04UbZx2_imu8&callback=initMap">
    </script></center>
</article>
</section>
<footer>
	<p>Copyright © 2019 ICTM1d Groep 4</p>
</footer>
</body>
</html>
