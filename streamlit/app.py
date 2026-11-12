# ==========================================
# IMPORT LIBRARIES
# ==========================================

import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="European EV Market Intelligence", page_icon="⚡", layout="wide"
)


# ==========================================
# LOAD DATASETS
# ==========================================

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the cleaned data directory
DATA_PATH = PROJECT_ROOT / "data" / "cleaned"

# Load datasets
ember_df = pd.read_csv(DATA_PATH / "ember_bev_clean.csv")
europe_df = pd.read_csv(DATA_PATH / "electric_vehicle_data.csv")
forecast_df = pd.read_csv(DATA_PATH / "ev_forecasts.csv")

# Convert forecast date to datetime format
ember_df["date"] = pd.to_datetime(ember_df["date"])
forecast_df["date"] = pd.to_datetime(forecast_df["date"])


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("⚡ EV Intelligence")

st.sidebar.markdown("Explore the European EV market.")

page = st.sidebar.radio(
    "Navigation",
    ["Market Overview", "Adoption Drivers", "Future Forecasts"],
)


# ==========================================
# PAGE CONTENT - NAVIGATION
# ==========================================

# ------------------------------------------
# MARKET OVERVIEW - NAVIGATION SECTION
# ------------------------------------------

if page == "Market Overview":

    st.title("European EV Market Overview")

    st.markdown("""
    Explore the development of battery electric vehicle adoption
    across European countries.
    """)

    # ******************************************
    # MARKET OVERVIEW - KEY PERFORMANCE INDICATORS
    # ******************************************

    # Use September 2026 as the common reporting month
    snapshot_date = "2026-09-01"

    europe_snapshot = ember_df[
        (ember_df["continent"] == "Europe") & (ember_df["date"] == snapshot_date)
    ].copy()

    # Calculate KPIs
    total_registrations = europe_snapshot["bev_registrations"].sum()
    average_market_share = europe_snapshot["bev_share_pct"].mean()
    countries_reporting = europe_snapshot["country"].nunique()

    # ******************************************
    # DISPLAY KEY METRICS
    # ******************************************

    col1, col2, col3 = st.columns(3)

    col1.metric("BEV Registrations", f"{total_registrations:,.0f}")

    col2.metric("Average Country BEV Share", f"{average_market_share:.2f}%")

    col3.metric("Countries Reporting", countries_reporting)

    st.caption(
    f"Data reference: September 2026 | "
    f"{countries_reporting} European countries"
)
    #st.caption("Data reference: September 2026 | 32 European countries")

    # ******************************************
    # INTERACTIVE EUROPEAN BEV MARKET MAP
    # ******************************************

    st.subheader("BEV Market Share Across Europe")

    # Prepare data for the map
    map_data = europe_snapshot[
        ["country", "country_code", "bev_registrations", "bev_share_pct"]
    ].copy()

    # Create interactive map
    fig = px.choropleth(
        map_data,
        locations="country_code",
        locationmode="ISO-3",
        color="bev_share_pct",
        hover_name="country",
        hover_data={
            "country_code": False,
            "bev_registrations": ":,.0f",
            "bev_share_pct": ":.2f",
        },
        labels={
            "bev_registrations": "BEV Registrations",
            "bev_share_pct": "BEV Market Share (%)",
        },
        color_continuous_scale="Blues",
        range_color=(0, 100),
        scope="europe",
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        coloraxis_colorbar={"title": "BEV Market Share (%)"},
    )

    fig.update_geos(fitbounds="locations", visible=True)

    # Display map in Streamlit
    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False})

    st.caption(
        "BEV market share represents the percentage of newly registered "
        "passenger cars that are battery electric vehicles. "
        "Grey countries have no available data for September 2026."
    )

    # ******************************************
    # TOP 10 COUNTRIES BY BEV MARKET SHARE
    # ******************************************

    st.subheader("Top 10 European Countries by BEV Market Share")

    # Select the 10 countries with the highest BEV market share
    top_10_share = (
        europe_snapshot.sort_values("bev_share_pct", ascending=False)
        .head(10)
        .sort_values("bev_share_pct", ascending=True)
    )

    # ******************************************
    # CREATE INTERACTIVE TOP 10 BAR CHART
    # ******************************************

    # Define the ranking order
    country_order = top_10_share.sort_values("bev_share_pct", ascending=False)[
        "country"
    ].tolist()

    # Create chart
    chart = (
        alt.Chart(top_10_share)
        .mark_bar()
        .encode(
            x=alt.X("bev_share_pct:Q", title="BEV Market Share (%)"),
            y=alt.Y("country:N", sort=country_order, title="Country"),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("bev_share_pct:Q", title="BEV Market Share", format=".2f"),
            ],
        )
        .properties(height=350)
    )

    st.altair_chart(chart, use_container_width=True)

    # ******************************************
    # HISTORICAL EUROPEAN BEV ADOPTION TREND
    # ******************************************

    st.subheader("European BEV Market Share Evolution (2023–2026)")

    # Calculate monthly average market share
    europe_monthly_trend = (
        ember_df[
            (ember_df["continent"] == "Europe")
            & (ember_df["date"] >= "2023-01-01")
            & (ember_df["date"] <= "2026-09-01")
        ]
        .groupby("date")
        .agg(
            average_bev_share=("bev_share_pct", "mean"),
            countries_reporting=("country", "nunique"),
        )
        .reset_index()
    )

    # Create interactive line chart
    trend_chart = (
        alt.Chart(europe_monthly_trend)
        .mark_line(color="#2878B5", strokeWidth=2)
        .encode(
            x=alt.X(
                "date:T",
                title="Month",
                axis=alt.Axis(format="%b %Y", tickCount=8, labelAngle=-45),
            ),
            y=alt.Y(
                "average_bev_share:Q",
                title="Average BEV Market Share (%)",
                scale=alt.Scale(domain=[10, 35]),
            ),
            tooltip=[
                alt.Tooltip("date:T", title="Month", format="%B %Y"),
                alt.Tooltip(
                    "average_bev_share:Q", title="Average BEV Share", format=".2f"
                ),
                alt.Tooltip("countries_reporting:Q", title="Countries Reporting"),
            ],
        )
        .properties(height=350)
    )

    st.altair_chart(trend_chart, use_container_width=True)

    st.caption(
        "Monthly unweighted average across reporting European countries. "
        "Period: January 2023 – September 2026."
    )

    # ******************************************
    # INDIVIDUAL COUNTRY ADOPTION TREND
    # ******************************************

    st.subheader("Explore Individual Country Adoption")

    # Create country selector
    selected_country = st.selectbox(
        "Select a country",
        sorted(ember_df["country"].unique()),
        index=sorted(ember_df["country"].unique()).index("Norway"),
    )

    # Filter data for selected country and period
    country_trend = ember_df[
        (ember_df["country"] == selected_country)
        & (ember_df["date"] >= "2023-01-01")
        & (ember_df["date"] <= "2026-09-01")
    ].copy()

    # DISPLAY COUNTRY DATA COVERAGE
    latest_country_date = pd.to_datetime(country_trend["date"].max())

    st.caption(
        f"Data available from January 2023 to "
        f"{latest_country_date.strftime('%B %Y')}."
    )

    # Create individual country line chart
    country_chart = (
        alt.Chart(country_trend)
        .mark_line(color="#E07A2D", strokeWidth=2)
        .encode(
            x=alt.X(
                "date:T",
                title="Month",
                axis=alt.Axis(format="%b %Y", tickCount=8, labelAngle=-45),
            ),
            y=alt.Y("bev_share_pct:Q", title="BEV Market Share (%)"),
            tooltip=[
                alt.Tooltip("date:T", title="Month", format="%B %Y"),
                alt.Tooltip("bev_share_pct:Q", title="BEV Market Share", format=".2f"),
            ],
        )
        .properties(title=f"BEV Adoption Trend – {selected_country}", height=350)
    )

    st.altair_chart(country_chart, use_container_width=True)

# ------------------------------------------
# ADOPTION DRIVERS - NAVIGATION SECTION
# ------------------------------------------

elif page == "Adoption Drivers":

    st.title("What Is Associated with EV Adoption?")

    st.markdown("""
    Exploring how charging infrastructure and economic conditions
    relate to battery electric vehicle adoption across Europe.
    """)

    # ==========================================
    # PREPARE 2025 DATA
    # ==========================================

    drivers_2025 = europe_df[europe_df["year"] == 2025].copy()

    # Calculate charging points per 100,000 inhabitants
    drivers_2025["charging_points_per_100k"] = (
        drivers_2025["charging_points"] / drivers_2025["population"]
    ) * 100000

    st.caption(
        "Reference year: 2025 | Country coverage varies "
        "depending on indicator availability."
    )

    # ==========================================
    # CHARGING INFRASTRUCTURE VS BEV ADOPTION
    # ==========================================

    st.subheader("Charging Infrastructure & BEV Adoption")

    charging_data = drivers_2025.dropna(
        subset=["charging_points_per_100k", "avg_monthly_bev_share_pct"]
    ).copy()

    charging_corr = charging_data["charging_points_per_100k"].corr(
        charging_data["avg_monthly_bev_share_pct"]
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        charging_chart = (
            alt.Chart(charging_data)
            .mark_circle(size=110, opacity=0.75)
            .encode(
                x=alt.X(
                    "charging_points_per_100k:Q",
                    title="Charging Points per 100,000 Inhabitants",
                ),
                y=alt.Y(
                    "avg_monthly_bev_share_pct:Q", title="Average BEV Market Share (%)"
                ),
                tooltip=[
                    alt.Tooltip("country:N", title="Country"),
                    alt.Tooltip(
                        "charging_points_per_100k:Q",
                        title="Charging Points per 100k",
                        format=".1f",
                    ),
                    alt.Tooltip(
                        "avg_monthly_bev_share_pct:Q",
                        title="BEV Market Share",
                        format=".2f",
                    ),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(charging_chart, use_container_width=True)

    with col2:

        st.metric("Pearson correlation (r)", f"{charging_corr:.2f}")
        st.metric("Countries included", charging_data["country"].nunique())

        st.markdown("**Key insight**")

        st.write(
            "Norway has a 95.6% BEV market share with 567 charging points per 100,000 residents. "
            "The Netherlands has 1,161 charging points but a 39.6% BEV market share."
        )

    st.caption(
        "Charging infrastructure is measured as public recharging "
        "points per 100,000 inhabitants. BEV market share represents "
        "the average monthly share of new passenger-car registrations."
    )

    st.divider()

    # ==========================================
    # GDP PER CAPITA VS BEV ADOPTION
    # ==========================================

    st.subheader("GDP per Capita & BEV Adoption")

    gdp_data = drivers_2025.dropna(
        subset=["gdp_per_capita", "avg_monthly_bev_share_pct"]
    ).copy()

    gdp_corr = gdp_data["gdp_per_capita"].corr(gdp_data["avg_monthly_bev_share_pct"])

    col1, col2 = st.columns([3, 1])

    with col1:

        gdp_chart = (
            alt.Chart(gdp_data)
            .mark_circle(size=110, opacity=0.75)
            .encode(
                x=alt.X("gdp_per_capita:Q", title="GDP per Capita (€)"),
                y=alt.Y(
                    "avg_monthly_bev_share_pct:Q", title="Average BEV Market Share (%)"
                ),
                tooltip=[
                    alt.Tooltip("country:N", title="Country"),
                    alt.Tooltip(
                        "gdp_per_capita:Q",
                        title="GDP per Capita (€)",
                        format=",.0f",
                    ),
                    alt.Tooltip(
                        "avg_monthly_bev_share_pct:Q",
                        title="BEV Market Share",
                        format=".2f",
                    ),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(gdp_chart, use_container_width=True)

    with col2:

        st.metric("Pearson correlation (r)", f"{gdp_corr:.2f}")
        st.metric("Countries included", gdp_data["country"].nunique())

        st.markdown("**Key insight**")

        st.write(
            "Norway reaches 95.6% BEV adoption. Luxembourg (27.1%), "
            "Ireland (28.8%) and Switzerland (22.4%) have considerably "
            "lower adoption despite higher GDP per capita."
        )

    st.caption(
        "GDP per capita values for 2025, measured in chain-linked euros. Source: Eurostat."
    )


# ------------------------------------------
# FUTURE FORECAST - NAVIGATION SECTION
# ------------------------------------------

elif page == "Future Forecasts":

    st.title("Future EV Adoption Forecasts")

    st.markdown("""
    Explore the projected development of battery electric vehicle
    market share across Europe over the next 12 months.
    """)

    # ******************************************
    # FORECAST OVERVIEW - KEY METRICS
    # ******************************************

    countries_forecasted = forecast_df["country"].nunique()
    forecast_months = forecast_df["date"].nunique()

    forecast_start = forecast_df["date"].min()
    forecast_end = forecast_df["date"].max()

    reference_date = forecast_start - pd.DateOffset(months=1)

    col1, col2, col3 = st.columns(3)

    col1.metric("Countries Forecasted", countries_forecasted)
    col2.metric("Forecast Horizon", f"{forecast_months} months")
    col3.metric("Latest Historical Data", reference_date.strftime("%B %Y"))

    st.caption(
        f"Forecast period: {forecast_start.strftime('%B %Y')} – "
        f"{forecast_end.strftime('%B %Y')}"
    )

    st.divider()

    # ******************************************
    # COUNTRY FORECAST EXPLORER
    # ******************************************

    st.subheader("Explore Individual Country Forecasts")

    countries = sorted(forecast_df["country"].unique())

    selected_country = st.selectbox(
        "Select a country",
        countries,
        index=countries.index("Norway")
    )

    # ******************************************
    # PREPARE HISTORICAL DATA
    # ******************************************

    historical_country = ember_df[
        (ember_df["country"] == selected_country)
        & (ember_df["date"] >= "2023-01-01")
        & (ember_df["date"] <= "2026-09-01")
    ].copy()

    historical_country["data_type"] = "Historical"
    historical_country["bev_share_display"] = historical_country["bev_share_pct"]

    # ******************************************
    # PREPARE FORECAST DATA
    # ******************************************

    country_forecast = forecast_df[
        forecast_df["country"] == selected_country
    ].copy()

    country_forecast["data_type"] = "Forecast"
    country_forecast["bev_share_display"] = (
        country_forecast["forecast_bev_share_pct"]
    )

    # Get selected forecasting model
    selected_model = country_forecast["forecast_model"].iloc[0]

    # ******************************************
    # HISTORICAL VS FORECAST CHART
    # ******************************************

    # Combine historical and forecast data
    chart_data = pd.concat(
        [
            historical_country[
                ["date", "bev_share_display", "data_type"]
            ],
            country_forecast[
                ["date", "bev_share_display", "data_type"]
            ]
        ],
        ignore_index=True
    )

    # Create historical and forecast line chart
    forecast_line = (
        alt.Chart(chart_data)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=alt.X(
                "date:T",
                title="Month",
                axis=alt.Axis(
                    format="%b %Y",
                    tickCount=10,
                    labelAngle=-45
                )
            ),
            y=alt.Y(
                "bev_share_display:Q",
                title="BEV Market Share (%)"
            ),
            color=alt.Color(
                "data_type:N",
                title="Data",
                scale=alt.Scale(
                    domain=["Historical", "Forecast"],
                    range=["#2878B5", "#E07A2D"]
                )
            ),
            tooltip=[
                alt.Tooltip(
                    "date:T",
                    title="Month",
                    format="%B %Y"
                ),
                alt.Tooltip(
                    "bev_share_display:Q",
                    title="BEV Market Share (%)",
                    format=".2f"
                ),
                alt.Tooltip(
                    "data_type:N",
                    title="Data Type"
                )
            ]
        )
    )

    # Add vertical line marking the beginning of the forecast
    forecast_boundary = (
        alt.Chart(
            pd.DataFrame({"date": [forecast_start]})
        )
        .mark_rule(
            color="#777777",
            strokeDash=[6, 4],
            strokeWidth=1.5
        )
        .encode(
            x="date:T"
        )
    )

    # Combine both charts
    forecast_chart = (
        alt.layer(forecast_line, forecast_boundary)
        .properties(
            title=f"Historical vs. Forecasted BEV Market Share – {selected_country}",
            height=400
        )
    )

    st.altair_chart(forecast_chart, use_container_width=True)

    # ******************************************
    # FORECAST MODEL EXPLANATION
    # ******************************************

    if selected_model == "Naive":
        st.caption(
            "Forecast uses the latest historical value for all future months."
        )

    elif selected_model == "Seasonal Naive":
        st.caption(
            "Forecast repeats the corresponding monthly values from the previous year."
        )

    else:
        st.caption(
            "Forecast models historical trends and seasonal patterns."
        )

    # ******************************************
    # FORECAST DETAILS
    # ******************************************

    # Calculate projected adoption momentum
    average_momentum = country_forecast["forecast_yoy_change_pp"].mean()

    latest_momentum = country_forecast.loc[
        country_forecast["date"].idxmax(),
        "forecast_yoy_change_pp"
    ]

    st.divider()

    st.caption("**Forecast Details**")

    col1, col2, col3 = st.columns(3)

    col1.metric("Selected Model", selected_model)

    col2.metric(
        "Average YoY Change",
        f"{average_momentum:+.2f} pp"
    )

    col3.metric(
        f"{forecast_end.strftime('%B %Y')} YoY Change",
        f"{latest_momentum:+.2f} pp"
    )

    # ******************************************
    # FORECAST LIMITATIONS
    # ******************************************

    with st.expander("Limitations & Data Notes"):

        st.markdown("""
        - **Historical data:** Forecasts may not capture sudden market changes.
        - **External factors:** Policies, prices and economic conditions are not included.
        - **Model selection:** Only three forecasting models were compared.
        - **Data quality:** Bulgaria's missing July 2026 value was interpolated.
        - **Forecast boundaries:** Predictions are limited to 0–100%.
        """)
