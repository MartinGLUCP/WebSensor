<?php
	$action = $_GET['action'];
	$connexion2 = new PDO('pgsql:host=postgresql-websensor.alwaysdata.net;port=5432;dbname=websensor_2019;user=websensor;password=projet2019');
	$connexion = new PDO('mysql:host=localhost;dbname=websensor', 'root', '');
	$resultset = $connexion->prepare("SELECT * FROM event");
	$resultset->execute();
	$count = $resultset->rowCount();
	$dataTweet = array();
	$tmpObj = array();
	while ($row = $resultset->fetch(PDO::FETCH_ASSOC)) {
		/*$tmpObj = [
			'vector' => strval($row["vector"]),
			'tweet_content' => strval($row["tweet_content"]),
			'id_tweet' => strval($row["id_tweet"]),
			'date' => strval($row["date"])
		];*/
		$tmpObj = [
			'label' => strval($row["label"]),
		];
		array_push($dataTweet, $tmpObj);
	}
	echo json_encode($dataTweet, JSON_PRETTY_PRINT);
	
?>

	