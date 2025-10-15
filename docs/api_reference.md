# Référence API

# Solaire

## Endpoint : `/predict/solaire`

> Prédit la production solaire à partir de l'irradiance globale et de la température

---

### Méthode HTTP

`POST`

---

### Corps de la requête (JSON)

| Champ                      | Type  | Description                        |
| -------------------------- | ----- | ---------------------------------- |
| `global_tilted_irradiance` | float | Irradiance globale inclinée (W/m²) |
| `temperature_2m`           | float | Température moyenne à 2 m (°C)     |

---

### Exemple de requête

```bash
POST /predict/solaire
Content-Type: application/json

{
  "global_tilted_irradiance": 450.2,
  "temperature_2m": 20,
}
```
---

### Réponse

```json
{"prediction": 532.41}
```
> Aucun traitement additionnel ni features dérivées nécessaires.

---

# Hydro-électrique

## Endpoint : `/predict/hydro`

---

### Méthode HTTP

`POST`

---

### Corps de la requête (JSON)

| Champ   | Type  | Description        |
| ------- | ----- | ------------------ |
| `QmnJ`  | float | Débit moyen (m³/s) |
| `HIXnJ` | float | Hauteur d’eau      |


---

### Exemple de requête

```bash
POST /predict/hydro
Content-Type: application/json

{
  "QmnJ": 25.3,
  "HIXnJ": 12.7,
}
```
### Réponse

```json
{"prediction": 131.55}

```
---

# Eolienne
## Endpoint : `/predict/eolienne`

> Prédit la production éolienne à partir de la vitesse moyenne du vent, le potentiel énergétique du vent et la densité de l'air

---

## Méthode HTTP

`POST`

---

### Corps de la requête (JSON)

| Champ | Type | Description | Contraintes |
|-------|------|--------------|--------------|
| `wind_speed_10m_mean` | `float` | Vitesse moyenne du vent à 10 mètres (m/s). | Doit être > 0 |
| `pressure_msl_mean` | `float` | Pression moyenne au niveau de la mer (hPa). | Doit être > 0 |
| `temperature_2m_mean` | `float` | Température moyenne à 2 mètres (°C). | Doit être > 0 |

---

### Exemple de requête

```bash
POST /predict/eolienne
Content-Type: application/json

{
  "wind_speed_10m_mean": 5.6,
  "pressure_msl_mean": 1013.2,
  "temperature_2m_mean": 18.4
}
```

### Traitement interne

Lorsqu'un requête est reçue :

1. Les trois entrées (wind_speed_10m_mean, pressure_msl_mean, temperature_2m_mean) sont validées.

2. Si l'une d'elles vaut 0, l'API renvoie une erreur.

3. Deux nouvelles features dérivées sont créées:

- wind_speed3 (variable qui exprime la réalité physique de la production d'énergie éolienne)
- temp_press (variable de densité de l'air)

4. Le modèle eolienne_random_forest_model.pkl est chargé via ModelTrain.load().

5. Le modèle effectue une prédiction de la production éolienne.

### Réponses

- Succès - 200 OK

```json
{
    "prediction": 127.53
}
```

### Erreur - 400 Bad Request

```json
{
    "error": "wind_speed_10m_mean, pressure_msl_mean et temperature_2m_mean doit être supérieur à 0"
}

```

### Notes techniques

- Le modèle est une Random Forest Regressor (scikit-learn).
- Les features dérivées améliorent la corrélation physique avec la production réelle.
- L'API est conçue pour être intégrée dans une interface Streamlit ou un autre client web de prédiction.
- Les prédictions sont instantanées et ne nécessitent pas d'accès à la base de données.

