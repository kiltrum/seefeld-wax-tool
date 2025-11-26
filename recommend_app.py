import streamlit as st
import pandas as pd

CLEAN_CSV = "wax_data_clean.csv"

# -------------------------------
# Load cleaned data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN_CSV)

    # Ensure numeric data
    df["air_temp"] = pd.to_numeric(df["air_temp"], errors="coerce")
    df["snow_temp"] = pd.to_numeric(df["snow_temp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["layers"] = pd.to_numeric(df["layers"], errors="coerce")

    return df


def recommend(location, air_temp, snow_type, snow_moisture):
    df = load_data()

    # Filter by location
    df_loc = df[df["location"] == location]
    if df_loc.empty:
        return None, "Keine Daten zum Standort."

    # Filter by temperature ±2°C
    df_temp = df_loc[
        (df_loc["air_temp"] >= air_temp - 2) &
        (df_loc["air_temp"] <= air_temp + 2)
    ]
    if df_temp.empty:
        return None, "Keine Daten für diesen Temperaturbereich."

    # Filter by snow type
    df_snow = df_temp[df_temp["snow_type"] == snow_type]
    if df_snow.empty:
        return None, "Keine Daten für diesen Schneetyp."

    # Filter by moisture
    df_moist = df_snow[df_snow["snow_moisture"] == snow_moisture]
    if df_moist.empty:
        return None, "Keine Daten für diese Schneefeuchte."

    # Group recommendations
    results = (
        df_moist.groupby(["wax_brand", "wax_product"])
        .agg(
            avg_rating=("rating", "mean"),
            count=("rating", "count"),
            avg_layers=("layers", "mean"),
        )
        .sort_values(by="avg_rating", ascending=False)
    )

    if results.empty:
        return None, "Keine Wachs-Daten gefunden."

    return results.head(5), None


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("⛷️ Seefeld Wax Recommendation")
st.write("Gib die Bedingungen ein und erhalte die Top-Wachsempfehlungen.")

df = load_data()

# Sidebar inputs
st.sidebar.header("Eingaben")

location = st.sidebar.selectbox("Streckenabschnitt", sorted(df["location"].unique()))
air_temp = st.sidebar.slider("Lufttemperatur (°C)", -15, 5, value=-5)
snow_type = st.sidebar.selectbox("Schneetyp", sorted(df["snow_type"].unique()))
snow_moisture = st.sidebar.selectbox("Schneefeuchte", sorted(df["snow_moisture"].unique()))

# Button
if st.sidebar.button("Empfehlung anzeigen"):
    results, error = recommend(location, air_temp, snow_type, snow_moisture)

    if error:
        st.error(error)
    else:
        st.success("Top Wax-Empfehlungen für die gegebenen Bedingungen:")
        st.dataframe(results.style.format({"avg_rating": "{:.2f}", "avg_layers": "{:.1f}"}))

# Show raw data
with st.expander("📄 Rohdaten anzeigen"):
    st.dataframe(df)
