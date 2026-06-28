# stay-and-charge

App Streamlit affichant sur une carte interactive des logements (hôtels, locations courte durée) et les bornes de recharge électrique à proximité.

## Stack

- Python 3.11+
- [Streamlit](https://streamlit.io) + pydeck pour la carte interactive
- Google Places API (logements)
- API Opendatasoft ODRÉ (bornes IRVE, open data, sans clé API)
- geopy pour le géocodage et le calcul de distances

## Fonctionnalités actuelles

- Recherche de logements par ville ou code postal via Google Places (jusqu'à 60 résultats, 3 pages)
- Bornes de recharge recherchées autour de chaque logement (pas du centre ville)
- Carte avec deux IconLayers (logements / bornes), tooltip au survol
- Panneau détail au clic sur un point
- Sidebar : ville/code postal, rayon de recherche, distance max des bornes
- Message d'avertissement si les résultats semblent éloignés de la ville recherchée

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copie `.env.example` en `.env` et renseigne ta clé Google Places :

```bash
cp .env.example .env
```

## Lancement

```bash
streamlit run app.py
```

## Structure

```
app.py                  # point d'entrée Streamlit
config.py               # constantes et paramètres par défaut
logging_manager.py      # configuration du logging
data/
  lodging.py            # appels Google Places (pagination 3 pages)
  charging_stations.py  # appels API Opendatasoft (IRVE)
  geocoding.py          # géocodage via Nominatim
  cache.py              # wrappers st.cache_data (TTL 1h)
services/
  geo.py                # calculs de distance, détection résultats éloignés
  station_finder.py     # recherche des bornes par logement
components/
  map_view.py           # carte pydeck + groupement des stations
  filters.py            # sidebar de filtres
  detail_panel.py       # panneau détail (st.dialog)
models/
  schemas.py            # dataclasses Lodging, ChargingStation
tests/
```

## Périmètre actuel

Phase 1 — France uniquement. Affichage et redirection vers les sites de réservation (pas de réservation intégrée).
