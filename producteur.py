from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd
from database_create import Database

class Producteur(ABC):
    def __init__(self, nom: str, puissance_nominale: int, db_manager: 'Database'):
        if not db_manager.energy_type:
            raise ValueError("L'instance de Database doit être initialisée un 'energy_type' spécifique.")
        self.nom = nom
        self.puissance_nominale = puissance_nominale
        self.db_manager = db_manager
        
        self.table_name = f"{db_manager.energy_type.lower()}_data"
        self.prod_column_name = f"{db_manager.energy_type}"
        
    @abstractmethod
    def get_training_features(self) -> List[str]:
        """
        Chaque type de producteur doit déclarer les colonnes qui serviront de features pour l'entrainement
        """
        pass
    
    def get_all_data_for_training(self) -> pd.DataFrame:
        """
        Va récupérer toutes les données dans la table pour 
        préparer l'entrainement
        """
        
        print(f"Chargement des données d'entraînement pour '{self.nom}' depuis la table '{self.table_name}'...")
        
        # On utilise le client Supabase qui est dans l'objet db_manager
        response = self.db_manager.client.table(self.table_name)\
                                        .select('*')\
                                        .order('date', desc=False)\
                                        .execute()

        if not response.data:
            print(f"Aucune donnée d'entraînement trouvée dans la table {self.table_name}.")
            return pd.DataFrame()
            
        df = pd.DataFrame(response.data)
        
        # Petits traitements finaux pour rendre le DataFrame prêt à l'emploi
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.drop(columns=['id'], errors='ignore') # Suppression de l'ID
        
        print(f"{len(df)} lignes de données chargées.")
        return df
    
    def get_production_history(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Cherche la production d'une installation sur une période donnée.

        """
        print(f"Récupération de l'historique de production pour '{self.nom}'...")
        
        response = self.db_manager.client.table(self.table_name)\
                                        .select(f'date, {self.prod_column_name}')\
                                        .gte('date', start_date)\
                                        .lte('date', end_date)\
                                        .order('date', desc=False)\
                                        .execute()
        
        if not response.data:
            return pd.DataFrame(columns=['date', self.prod_column_name])
            
        return pd.DataFrame(response.data)
    
    def get_stats(self, start_date: str, end_date: str) -> Dict[str, float]:
        """ 
        Réutilisation de la méthode get_production_history pour calculer des stats
        """
        df_prod = self.get_production_history(start_date, end_date)
        
        if df_prod.empty:
            return {'moyenne': 0, 'max': 0, 'min': 0, 'total': 0, 'jours': 0}
        
        productions = df_prod[self.prod_column_name]
        
        stats = {
            'moyenne': productions.mean(),
            'max': productions.max(),
            'min': productions.min(),
            'total': productions.sum(),
            'jours': len(productions)
        }
        return {key: round(value, 2) for key, value in stats.items()}
    

class ProductionEolien(Producteur):
    def get_training_features(self):
        return ['wind_speed_10m_mean (km/h)', 'wind_speed3', 'temp_press']
    
class ProductionSolaire(Producteur):
    def get_training_features(self):
        return ['irradiance', 'temperature']

class ProductionHydro(Producteur):
    def get_training_features(self):
        return ['QmnJ', 'HIXnJ']