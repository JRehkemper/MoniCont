<html>
<head>
    <title>Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<style>
.wrapper{

}
.ContainerCard {
    width: 460px;
    padding: 2em;
    margin: 50px;
    background-color: tomato;
    border-radius: 15px;
    float:left;
    box-shadow: 0px 0px 15px 0px grey;
}
.ContainerCard a {
    text-decoration: none;
    color: black;
}

.ContainerCard a:hover {
    color: grey;
}
</style>
<body>
<div class="header">
    <h1>Monitoring LXD Container</h1>
</div>
<div class="wrapper">

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

    $sql = "SELECT * FROM MainMonitoring ORDER BY Name asc;";
    $result = mysqli_query($conn, $sql);

    if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        //echo "id: " . $row["id"]. " - Name: " . $row["cpu"]. " " . $row["ram"]. "<br>";

        echo '<div class="ContainerCard">';
        echo '<h2><a href="table.php?name=' . $row["name"] . '">' . $row["name"] . "</a></h2>";
        echo '<h3>' . $row["ip"] . "</h3>";
        echo '</div>';
    }
    } else {
    echo "0 results";
    }

    $conn->close();
    ?>
</div>
</body>
</html>
