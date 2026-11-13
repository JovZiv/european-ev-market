# ⚡🚗 European EV Market Intelligence 🌍🔋

An analysis of battery electric vehicle (BEV) adoption across Europe, exploring market trends, factors associated with adoption, and country-level forecasts for the next 12 months. The project includes an interactive Streamlit dashboard.

**[Open the live dashboard](https://european-ev-marketgit-final-project.streamlit.app/)**

## 📌 Project Overview

The project investigates how the European market for fully electric passenger cars is developing and what recent adoption patterns may suggest for the near future.

The analysis focuses on three areas:

1. **Market Overview** – BEV registrations, market shares, country rankings and adoption trends.
2. **Adoption Drivers** – The relationship between BEV market share, public charging infrastructure and GDP per capita.
3. **Future Forecasts** – Comparison of time-series forecasting methods and 12-month country-level projections.

The scope is limited to **battery electric passenger cars (BEVs)**. Hybrid vehicles are excluded.

## 📊 Key Findings

The market overview uses September 2026 as its reference month:

- **418,309** new BEV registrations across the countries included in the analysis.
- **31.85%** average country BEV market share.
- **32** countries reporting data.

The 31.85% figure is an **unweighted average**: each country's market share contributes equally, regardless of the size of its passenger-car market. It should not be interpreted as the combined market share across all registrations.

The 2025 country-level analysis found positive associations between BEV market share and:

- **Public charging points per 100,000 inhabitants:** Pearson correlation *r* = **0.71**.
- **GDP per capita:** Pearson correlation *r* = **0.60**.

These correlations indicate relationships, not proof that either factor directly causes higher BEV adoption.

## 🔮 Forecasting Approach

Three forecasting methods were compared separately for each country:

- **Naive:** Repeats the latest observed value.
- **Seasonal Naive:** Repeats the value from the same month in the previous year.
- **Holt-Winters:** Accounts for the current level, trend and seasonality.

The forecasting workflow was:

1. Train the models using historical data through **September 2025**.
2. Test predictions against actual market shares from **October 2025 to September 2026**.
3. Compare model performance using **Mean Absolute Error (MAE)**. A lower MAE indicates smaller average prediction errors.
4. Select the model with the lowest MAE for each country.
5. Refit each selected model using data through **September 2026** and forecast **October 2026 to September 2027**.

### Model Selection Results

| Selected method | Countries | Share of countries |
|---|---:|---:|
| Holt-Winters | 17 | 53.1% |
| Naive | 13 | 40.6% |
| Seasonal Naive | 2 | 6.3% |

The forecasts are estimates based on historical patterns. They are not guarantees of future market development.

## 💻 Interactive Dashboard

The Streamlit dashboard contains three sections:

### 1. Market Overview

- Key figures for BEV registrations, average country market share and reporting countries.
- Interactive map showing BEV market share across Europe.
- Top 10 countries by BEV market share.
- Historical European adoption trend and an individual country trend explorer.

### 2. Adoption Drivers

- Country-level comparison of charging infrastructure and BEV adoption.
- Country-level comparison of GDP per capita and BEV adoption.
- Pearson correlation values for both relationships.

### 3. Future Forecasts

- Select a country and compare its historical BEV market share with the 12-month forecast.
- View the forecasting method selected for that country.
- Explore projected year-on-year changes.

## 📂 Data Sources

The project combines data from the following sources:

- **[Ember](https://ember-energy.org/)** – Monthly BEV registrations and market shares.
- **[Eurostat](https://ec.europa.eu/eurostat/)** – Passenger-car registrations, population and economic indicators. The analysis uses the Eurostat dataset `ROAD_EQR_CARPDA` for registrations by country and fuel type.
- **[European Alternative Fuels Observatory (EAFO)](https://alternative-fuels-observatory.ec.europa.eu/)** – Alternative-fuel vehicle and charging infrastructure data.


## 🗂️ Repository Structure

```text
ev_adoption_project/
│
├── data/
│   ├── cleaned/
│   │   ├── electric_vehicle_data.csv
│   │   ├── ember_bev_clean.csv
│   │   └── ev_forecasts.csv
│   │
│   └── raw/
│       ├── ember_monthly_ev_sales.csv
│       ├── eurostat_charging_infrastructure.csv
│       ├── eurostat_electricity_prices.csv
│       ├── eurostat_gdp_per_capita.csv
│       ├── eurostat_population.csv
│       └── eurostat_vehicle_registrations.csv
│
├── notebooks/
│   ├── 01_ember_exploration.ipynb
│   ├── 02_registrations_exploration.ipynb
│   ├── 03_charging_infrastructure.ipynb
│   ├── 04_economic_indicators.ipynb
│   ├── 05_data_cleaning_and_integration.ipynb
│   ├── 06_electric_vehicle_analysis.ipynb
│   └── 07_electric_vehicle_forecasting.ipynb
│
└── streamlit/
    ├── app.py
    └── helper.ipynb
```

The Streamlit app reads the three cleaned CSV files from `data/cleaned/`.

## ⚙️ Run the Dashboard Locally

### 1. Clone the repository

```bash
git clone https://github.com/JovZiv/european-ev-market.git
cd european-ev-market
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required packages

```bash
python -m pip install -r requirements.txt
```

The dashboard uses Streamlit, pandas, Altair and Plotly.

### 4. Check the data files

Make sure these files are available in `data/cleaned/`:

- `ember_bev_clean.csv`
- `electric_vehicle_data.csv`
- `ev_forecasts.csv`

### 5. Start the application

```bash
streamlit run streamlit/app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser to use the dashboard.


## 🔗 Project Links

- **Live Dashboard:** https://european-ev-marketgit-final-project.streamlit.app/
- **Presentation Slides:** [https://google-slides-european-ev-market](https://drive.google.com/file/d/1ViYM76FywOL3r2XCZh5kr-Swd1qQy13a/view?usp=sharing)
