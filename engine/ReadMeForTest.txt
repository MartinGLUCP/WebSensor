Lancer le test avec les commandes suivantes :

DBSCAN :

1-DBSCAN avec vocabulaire pré-def et jeu de données de créé de 700 mots :

python test_clustering_tweets.py --dbscan

2-DBSCAN avec vocabulaire pré-def et jeu de données 9998 tweets :

python test_clustering_tweets.py --dbscan --use-mongodb

3-DBSCAN sans vocabulaire pré-def et jeu de données 9998 tweets :

python test_clustering_tweets.py --dbscan --use-mongodb --no-vocabulary


Mean Shift :

1-Mean shift avec vocabulaire pré-def et jeu de données de créé de 700 mots :

python test_clustering_tweets.py

2-Mean shift avec vocabulaire pré-def et jeu de données 9998 tweets :

python test_clustering_tweets.py --use-mongodb

3-Mean shift sans vocabulaire pré-def et jeu de données 9998 tweets :

python test_clustering_tweets.py --use-mongodb --no-vocabulary