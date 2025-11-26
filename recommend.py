import pandas as pd

CLEAN_CSV = "wax_data_clean.csv"

def load_data():
    df = pd.read_csv(CLEAN_CSV)

    # Erwartete Spalten:
    # timestamp, location, air_temp, snow_type, snow_moisture,
    # brand, product, rating, snow_temp, layers

    # numerisch erzwingen
    df["air_temp"] = pd.to_numeric(df["air_temp"], errors="coerce")
    df["snow_temp"] = pd.to_numeric(df["snow_temp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["layers"] = pd.to_numeric(df["layers"], errors="coerce")

    return df


def recommend(location, air_temp, snow_type, snow_moisture):
    df = load_data()

    # ------------------------
    # 1. Filter nach Standort
    # ------------------------
    df_loc = df[df["location"] == location]

    if df_loc.empty:
        return f"Keine Daten für Standort: {location}"

    # --------------------------------------
    # 2. Temperaturfilter (± 2 °C Toleranz)
    # --------------------------------------
    df_temp = df_loc[
        (df_loc["air_temp"] >= air_temp - 2) &
        (df_loc["air_temp"] <= air_temp + 2)
    ]

    if df_temp.empty:
        return f"Keine Daten für Temperaturbereich (~{air_temp}°C)."

    # -------------------------
    # 3. Schneetyp filtern
    # -------------------------
    df_snow = df_temp[df_temp["snow_type"] == snow_type]

    if df_snow.empty:
        return "Keine Daten für diesen Schneetyp."

    # -------------------------
    # 4. Schneefeuchte filtern
    # -------------------------
    df_moist = df_snow[df_snow["snow_moisture"] == snow_moisture]

    if df_moist.empty:
        return "Keine Daten für diese Schneefeuchte."

    # -------------------------
    # 5. Gruppieren und bewerten
    # -------------------------
    results = (
        df_moist.groupby(["wax_brand", "wax_product"])
        .agg(
            avg_rating=("rating", "mean"),
            count=("rating", "count"),
            avg_layers=("layers", "mean")  
        )
        .sort_values(by="avg_rating", ascending=False)
    )

    if results.empty:
        return "Keine Wax-Daten nach Gruppierung gefunden."

    return results.head(5)


if __name__ == "__main__":
    print("### Wax-Empfehlungstest ###")

    result = recommend(
        location="Möserer Steig",
        air_temp=0,
        snow_type="fresh_cold",
        snow_moisture="dry"
)
print(result)

