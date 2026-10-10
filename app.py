import pandas as pd
import streamlit as st

SQFT_PER_SQM = 10.7639

st.set_page_config(page_title="NYC Home Price Estimator")
st.title("NYC Home Price Estimator")
st.write("Estimate a home price range by borough, year, and area.")

forecasts = pd.read_csv("forecast_ranges.csv")
forecasts["Sale Year"] = pd.to_numeric(
    forecasts["Sale Year"]
).astype(int)

boroughs = sorted(forecasts["Borough"].dropna().unique())
years = sorted(forecasts["Sale Year"].dropna().unique())

borough = st.selectbox(
    "Borough",
    options=boroughs,
    accept_new_options=False,
)

year = st.selectbox(
    "Forecast year",
    options=years,
    accept_new_options=False,
)

area_sqm = st.number_input(
    "Home area (square meters)",
    min_value=20.0,
    max_value=1000.0,
    value=140.0,
    step=5.0,
)

if st.button("Estimate price"):
    matching_rows = forecasts[
        (forecasts["Borough"] == borough)
        & (forecasts["Sale Year"] == year)
    ]

    if matching_rows.empty:
        st.error("No forecast is available for this borough and year.")
    else:
        row = matching_rows.iloc[0]
        area_sqft = area_sqm * SQFT_PER_SQM

        estimated_price = row["forecast_price_per_sqft"] * area_sqft
        lower_price = row["lower_price_per_sqft"] * area_sqft
        upper_price = row["upper_price_per_sqft"] * area_sqft

        st.subheader("Estimated price range")
        st.write(f"**Borough:** {borough}")
        st.write(f"**Year:** {year}")
        st.write(f"**Area:** {area_sqm:.1f} m² ({area_sqft:,.0f} sq ft)")
        st.metric("Estimated price", f"${estimated_price:,.0f}")
        st.write(
            f"Approximate range: **${lower_price:,.0f}–${upper_price:,.0f}**"
        )
        st.caption(
            "This is a borough-level estimate based on historical sales. "
            "It is not a property appraisal or a guaranteed price."
        )