# stay-and-charge

App Streamlit affichant sur une carte interactive des logements (hôtels, locations courte durée) et les bornes de recharge électrique à proximité.

## Stack

- Python 3.11+
- [Streamlit](https://streamlit.io) + pydeck pour la carte
- Google Places API (logements)
- Données IRVE open data (bornes de recharge, France)

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copie `.env.example` en `.env` et renseigne tes clés :

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
config.py               # constantes et clés API
data/                   # accès aux données externes
services/               # géocodage, calcul de distances
components/             # carte pydeck, filtres sidebar
models/                 # dataclasses Lodging, ChargingStation
tests/
```

## Périmètre actuel

Phase 1 — France uniquement. Affichage et redirection vers les sites de réservation (pas de réservation intégrée).
