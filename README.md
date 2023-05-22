# WebSensor

## Objectif
L’objectif du projet est de développer une application, qui utilise les réseaux sociaux, en l'occurrence twitter, comme une source d’information à grande échelle, où chaque utilisateur est l’équivalent d’un capteur. En effet, on considère que chaque utilisateur qui poste du contenu sur twitter apporte une information, qui sera jugée pertinente ou non par l’application, et qui pourra être associée à d’autres tweets similaires afin de pouvoir repérer les différents events dont parlent les utilisateurs de twitter. Chaque tweet est donc bien traité comme s'il s'agissait d’une mesure effectuée par un capteur, et l’ensemble des tweets récupérés permettent l’étude des tendances globales. On peut faire une analogie avec la météo par exemple, et comparer chaque tweet avec un relevé de température. Un relevé seul apporte peu d’informations et n’est pas forcément fiable, mais lorsqu’on a des milliers de relevées répartis à la fois sur une zone géographique (Qui sera pour nous la France) ainsi qu’une durée, on peut créer des modèles qui permettent un traitement de ces données fiables.

### Fonctionnalités clés

- **Recherche d’events :** L’utilisateur pourra rechercher un event de plusieurs façons différentes.
- **Visualisation d’events :** L’utilisateur pourra visualiser les events depuis le site web. Ces events sont extraits à partir du réseau social twitter grâce à une analyse du texte de chaque tweet ainsi qu’à leur popularité. En effet les events proposés sur le site seront les plus pertinents sur le réseau social.
- **Comparaison d’events :** L’utilisateur peut comparer la popularité des événements sur une période donnée. Le résultat de la comparaison sera affichée sous forme de différents graphiques en courbe.
- **Visualisation et prédiction des events les plus populaires :** Chaque jour, un “top 10” des events les plus populaires sera mis en place, ce qui permettra à l’utilisateur de pouvoir voir un classement des events du jour. De plus, un système de prédiction de classement sera mis en place pour estimer quels sont les events qui peuvent prétendre au haut du classement pour la journée suivante.


## Algorithmes

### Traitement de texte brute

Data scrapping (100k tweets), Nettoyage data (stop word,lemmatisation...), tf-idf...

###  Clustering des données

DBSCAN, MeanShift avec tests

###  Prédiction 

ARIMA (déterminer les trends et évenements)

## Application
L’application sera accessible pour les utilisateurs via un site web.

## Rapport
Pour plus de détail voir rapport et présentation. Une démonstration est disponible en vidéo.

## Auteur
- Martin Guilbert Lejeune (mguilbertlejeune@gmail.com)
- Mathieu Voisin (mvoisin@hotmail.fr)
- Gabriel Chevalier (gabrielchevallier78@gmail.com)
- Lydia Khelfane (lydia.khelfane@etu.u-cergy.fr)
