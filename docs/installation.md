# Installation

## Cloner le projet
```
git clone https://github.com/GaetanCSimplon/production_enr.git

cd production_enr
```
## Créer et activer un environnement virtuel

```
python -m venv .venv
source .venv/bin/activate    # (Linux/Mac)
.venv\Scripts\activate       # (Windows)
```
## Installer les dépendances

```
uv sync
```

## Connexion à fastapi
```
cd backend/app/
uv run --active fastapi dev main.py
```

## Connexion à l'interface Streamlit

```
cd frontend/
streamlit run app.py
```