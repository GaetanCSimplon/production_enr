i# production_enr
Projet de prédiction de production d'énergie

Mémo : 


Prétraitement

1 - Traiter csv avec production (date + prod)
2 - Récupérer via API les paramètres météo (param météo) en lien avec le type de production
3 - Traitement des données météo pour en faire des variables utilisable dans le ML
4 - Fusion des données du csv_prod et paramètre météo
5 - Implémentation dans la base de données

Classe

1 - Classe pour gestion des données (DataHandler)
2 - Classe enfant CSVDataHandler, APIDataHandler
3 - Classe ModelTrainer (destiné à la phase de modélisation)
4 - Classe pour gestion de la BDD - DataBase() (3 méthodes, create_table, drop_table, fetch_data)
5 - Classe Producteur (abstraite) -> ProducteurEolienne, ProducteurSolaire, ProducteurHydro

Modélisation

1 - Sélection des features et target (X, y)
2 - Split temporel 
3 - Sélection du modèle (à choisir entre RF et XGB)
4 - Optimisation des hyperparamètres (RandomizedSearchCV, TimeSeriesSplit et fit())
5 - Prédictions (predict)
6 - Evaluations des performances (r2 train, r2 test, MAE, MSE, RMSE)
7 - Validation croisée temporelle
8 - Sauvegarde du modèle (.pkl)
9 - Retour des résultats 
