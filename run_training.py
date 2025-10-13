import os
from dotenv import load_dotenv
import argparse
from database_create import Database
from producteur import ProductionEolien, ProductionHydro, ProductionSolaire, Producteur 
from model_trainer import ModelTrainer


PRODUCER_CONFIG = {
    "eolienne": {
        "class": ProductionEolien,
        "nom": "Eolienne",
        "puissance": 100
    },
    "solaire": {
        "class": ProductionSolaire,
        "nom": "Solaire",
        "puissance": 150
    },
    "hydro": {
        "class": ProductionHydro,
        "nom": "Hydro-Electrique",
        "puissance": 200
    }
}

def main(energy_type: str):
    print(f"--- Démarrage du script d'entrainement pour le modèle : {energy_type.upper()} ---")
    
    # Chargement des variables d'environnement
    load_dotenv()
    
    db_url = os.getenv("DATABASE_URL")
    supabase_url = os.getenv("SUPABASE_URL")
    

    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY ") 
    
    if not all([db_url, supabase_url, supabase_key]):
        raise ValueError("Une ou plusieurs variables d'environnement manquantes. Vérifiez votre fichier .env et les noms des variables.")
    
    # Connexion à la BDD
    print("\n[1/4] Connexion à la base de données...")
    db_manager = Database(
        url=supabase_url,
        service_key=supabase_key,
        database_url=db_url,
        energy_type=energy_type
    )
    print('Connexion établie.')
    
    # Instance de classe Producteur
    print("\n[2/4] Initialisation du fournisseur de données (Producteur)...")
    config = PRODUCER_CONFIG[energy_type]
    ProducerClass = config["class"]
    producer = ProducerClass(
        nom=config['nom'],
        puissance_nominale=config['puissance'],
        db_manager=db_manager
    )
    print(f"Producteur '{producer.nom}' prêt.")
    
    # Récupération des données d'entrainement
    print("\n[3/4] Récupération des données depuis la base de données...")
    training_data = producer.get_all_data_for_training()
    
    if training_data.empty:
        print("Entrainement annulé : aucune donnée trouvée.")
        return
    print(f"{len(training_data)} lignes de données récupérées.")
    
    # Entrainement du modèle (instance ModelTrainer)
    print("\n[4/4] Préparation et lancement de l'entraînement du modèle...")
    
    features = producer.get_training_features()
    target = producer.prod_column_name
    
    trainer = ModelTrainer(
        producer_type=energy_type, # C'est bien la variable dynamique ici, parfait.
        features=features,
        target=target,
        save_dir='saved_models'
    )
    
    print("   - Configuration du trainer terminée.")
    print(f"   - Lancement de l'entraînement pour {energy_type.upper()}...")
    
    trainer.train(data=training_data)
    
    print("\n Entrainement terminé avec succès !")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script d'entrainement pour les modèles de prédictions d'énergie.")
    parser.add_argument(
        "energy_type",
        type=str,
        choices=PRODUCER_CONFIG.keys(),
        help="Choisir entre 'eolienne', 'solaire', 'hydro'"
    )
    
    args = parser.parse_args()
    main(args.energy_type)