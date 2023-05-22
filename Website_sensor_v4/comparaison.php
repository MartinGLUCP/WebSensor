<?php
session_start();
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Accueil</title>
    <meta charset="UTF-8">
  	<meta http-equiv="X-UA-Compatible" content="IE=edge">
  	<meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="css/style2.css">    
</head>
<body>
<?php
	require ('include/header.inc.php');
	headWeb("Index","Gestion de l'apprentissage","home","index");
?>

<div class="page">
<section id="main">
	<div class="searchbar">
                               
    <div class="navbar-form collapse navbar-collapse">
       <form class="pieform header-search-form" name="usf" method="post" action="index.php" id="usf">
      <div><span id="usf_query_container" class="form-group-inline">
        <label class="sr-only" for="usf_query">Search</label>
  <input type="text" class="form-control text" id="usf_query" name="query" placeholder="Search" tabindex="0" value=""></span>
  <span id="usf_submit_container" class="form-group-inline">
    <button type="submit"  class="btn-default input-group-btn button btn" id="usf_submit" name="submit" tabindex="0">
      <span class="icon icon-search icon-lg" role="presentation" aria-hidden="true"></span><span class="sr-only">Goooooo</span>
    </button></span></div><input type="hidden" class="hidden" id="usf_sesskey" name="sesskey" value="">
<input type="hidden" name="pieform_usf" value="ff">
        </form>

        </div>
    </div>
    <div class="event-comparaison">

      <ul>Liste d'events à comparer :
        <li>event n°1 : </li>
        <li>event n°2 :</li>
        <li>event n°3 : </li>

      </ul>
    </div>
<div class="comparaison-graph">
  <p> Graph
  </p>

</div>

<div class="informations-event">

      <ul>Informations sur l'event :
        <li>Nom : </li>
        <li>Catégorie :</li>
        <li>Lieu : </li>
        <li> Date : </li>
        <li>Popularité : </li>
        <li> Tweet Populaire : </li>

      </ul>
    </div>

</section>
</div>
<?php
require("include/footer.inc.php");
  foot();
  ?>
