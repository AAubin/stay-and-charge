# stay-and-charge

App Streamlit affichant sur une carte interactive des logements (hôtels, locations courte durée) et les bornes de recharge électrique à proximité.

## Stack

- Python 3.11+
- [Streamlit](https://streamlit.io) + pydeck pour la carte interactive
- Google Places API (logements)
- API Opendatasoft ODRÉ (bornes IRVE, open data, sans clé API)
- Google Geocoding API (géocodage ville/code postal)
- geopy pour le calcul de distances

## Fonctionnalités

- Recherche de logements par ville ou code postal via Google Places (jusqu'à 60 résultats, 3 pages)
- Bornes de recharge recherchées autour de chaque logement (pas du centre ville)
- Carte interactive avec deux IconLayers (logements / bornes), tooltip au survol, panneau détail au clic
- Vue liste en complément de la carte (logements triés, bornes associées)
- Filtres : rayon de recherche, distance max des bornes, note minimale, type de prise, puissance minimale
- Message d'avertissement si les résultats semblent éloignés de la ville recherchée
- URL partageable avec les paramètres de recherche

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
# prod uniquement
pip install -r requirements.txt
# avec les dépendances de dev (tests)
pip install -r requirements-dev.txt
```

Copie `.env.example` en `.env` et renseigne ta clé Google Places :

```bash
cp .env.example .env
```

## Lancement

```bash
streamlit run app.py
```

## Tests

```bash
# tests unitaires uniquement
pytest -m "not integration"
# tous les tests (unitaires + intégration, nécessite une connexion réseau et la clé Google Places)
pytest
```

## Structure

```
app.py                  # point d'entrée Streamlit
config.py               # constantes et paramètres par défaut
logging_manager.py      # configuration du logging
data/
  lodging.py            # appels Google Places (pagination 3 pages)
  charging_stations.py  # appels API Opendatasoft (IRVE)
  geocoding.py          # géocodage via Google Geocoding API
  cache.py              # wrappers st.cache_data (TTL 1h)
services/
  geo.py                # calculs de distance, détection résultats éloignés
  station_finder.py     # association logements <-> bornes, filtres, agrégation
components/
  map_view.py           # carte pydeck + groupement des stations
  list_view.py          # vue liste logements / bornes
  filters.py            # sidebar de filtres
  render_details.py     # panneau détail au clic (st.dialog) et cards bornes
models/
  schemas.py            # dataclasses Lodging, ChargingStation
tests/
  unit_tests/           # tests unitaires (pytest)
  integration_tests/    # tests d'intégration (appels réseau réels)
```

## Périmètre actuel

Phase 1 — France uniquement. Affichage et redirection vers les sites de réservation (pas de réservation intégrée).
