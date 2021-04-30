<!DOCTYPE HTML>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
  <title>Monitoring LXD Container</title>
</head>
<body>
<div class="header">
<h1>Monitoring LXD Container</h1>
</div>
<a style="width: 100%; margin: 5em;" href="Dashboard.php">zurück zum Dashboard</a>
<div class="Tabellewrapper">

<table id="t01">
	  <tr>
	  	<th>Timestamp</th>
		<th>Name</th>
		<th>IP</th> 
		<th>CPU (%)</th>
		<th>RAM (MB)</th>
		<th>Swap (MB)</th>
		<th>Processes</th>	
		<th>Uptime (Min)</th>
	  </tr>
<?php

error_reporting(E_ERROR | E_WARNING | E_PARSE);
$servername = "jrehkemper.de:13306";
$username = "dbuser";
$password = "dbpassword";
$dbname = "monicont";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
    echo "Connection failed";
}



//$sql = "SELECT * FROM darling_wallaby Join MainMonitoring On darling_wallaby.name=MainMonitoring.name Order By timestamp desc Limit 5;";
$urlparam = htmlspecialchars($_GET["name"]);
$sql = "SELECT * FROM ". $urlparam . " Join MainMonitoring On " . $urlparam . ".name=MainMonitoring.name Order By timestamp desc Limit 100;";
$result = mysqli_query($conn, $sql);

echo "<caption><h2>" . $urlparam . "</h2></caption>";
if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    //echo "id: " . $row["id"]. " - Name: " . $row["cpu"]. " " . $row["ram"]. "<br>";

	echo "<tr>";
	echo "<td>" . $row['timestamp'] . "</td>";
	echo "<td>" . $row['name'] . "</td>";
	echo "<td>" . $row['ip'] . "</td>";
	echo "<td>" . $row['cpu'] . "</td>";
	echo "<td>" . $row['ram'] . "</td>";
	echo "<td>" . $row['swap'] . "</td>";
	echo "<td>" . $row['processes'] . "</td>";
	echo "<td>" . $row['uptime'] . "</td>";
	echo "</tr>";
  }
} else {
  echo "0 results";
}

$conn->close();



?>
</table>

</div>

</body>
</html>
