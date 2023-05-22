<?php
function avatarAleatoire(){
$max = 12; //C'est le nombre de photo max !
$ext = 'png'; //C'est l'extension des photos
$path = 'img/avatar/';
$photo = "";
$photo .= '<img src="'.$path.'avatar_'.mt_rand(1, $max).'.'.$ext.'">';
return "$photo";
}
?>
