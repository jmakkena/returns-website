# Returns Website

Polished Streamlit MVP for an Amazon-style returns marketplace. It includes searchable mock inventory, shopping-assistant deal guidance, dashboard metrics, and presentation-friendly styling.

## Features

- Search with natural phrases like `headphones under $200`
- Category, condition, and budget filters
- Shopping assistant recommendations
- Dashboard cards for recovered value, average discount, and matched items
- Mock inventory stored separately in `data/inventory.json`

## Run locally

```powershell
cd "C:\Users\jdaaw\OneDrive\Documents\New project 2\returns-website"
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Files

- `app.py`: Streamlit entry point
- `components.py`: reusable UI rendering helpers
- `helpers.py`: filtering, assistant, and formatting logic
- `data/inventory.json`: mock returned-inventory dataset

## Demo flow

1. Search `headphones under $200`
2. Show the assistant panel suggestions
3. Toggle `Electronics` and `Like New`
4. Walk through the dashboard stats
5. Open the product cards and explain the savings and condition details

## Deploy

This app is ready for Streamlit Community Cloud or any Python hosting platform that supports Streamlit.
