# Utilisation

## Via interface

1. Choisir le type d’énergie (éolienne, solaire, hydro)

2. Renseigner les variables météo :

- Éolien → wind_speed, temperature, pression

3. L’application calcule automatiquement :

- wind_speed3 = wind_speed ** 3

- temp_press = temperature * pression

4. L’API FastAPI envoie ces données au modèle entraîné

5. Le résultat (production prédite) est affiché dans Streamlit

## Modèle de prédiction

| Énergie  | Variables d’entrée                                                                             | Modèle utilisé   |
| -------- | ---------------------------------------------------------------------------------------------- | ---------------- |
| Éolienne | `wind_speed_10m_mean`, `pressure_msl_mean`, `temperature_2m_mean`, `wind_speed3`, `temp_press` | Random Forest    |
| Solaire  | `global_tilted_irradiance`, `temperature_2m`                                                   | Ridge Regression |
| Hydro    | `QmnJ`, `HIXnJ`                                                                                | Random Forest    |

## Entraîner les modèles

Pour réentrainer un modèle :

```
# Pour la production éolienne
python backend/app/train_model.py eolienne
# Pour la production solaire
python backend/app/train_model.py solaire
# Pour la production hydro-électrique
python backend/app/train_model.py hydro
```
- Le modèle est sauvegardé automatiquement après entraînement dans le dossier saved_models