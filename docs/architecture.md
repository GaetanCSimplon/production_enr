## Architecture du projet

──

```bash
production_enr/
|──backend/
|  |──app/
|     |──routes/
|        |──eolienne.py
|        |──hydro.py
|        |──solaire.py
|     |──main.py           # App FastAPI
|     |──model_trainer.py  # Classe d'entraînement des modèles
|     |──train_models.py   # Script principal d'entraînement
|  |──saved_models/        # Dossier de sauvegarde des modèles
|──docs/       # Documentation du projet
|──frontend/
|  |──pages
|     |──Hydro.py
|     |──Solar.py
|     |──Wind.py
|  |──app.py               # Interface streamlit
|──handlers/
|  |──datahandler.py       # Classe de gestion des données 
|──notebooks/
|  |──notebook_prod_eolienne.ipynb
|  |──notebook_prod_hydro.ipynb
|  |──notebook_samy.ipynb  # Analyse des données de production solaire
|  |──notebook_select_model.ipynb
|──mkdocs.yaml             # Fichier de configuration de documentation
```