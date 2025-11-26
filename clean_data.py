import pandas as pd

INPUT_FILE = "wax_data_seefeld.csv"
OUTPUT_FILE = "wax_data_clean.csv"

def clean_data():
    df = pd.read_csv(INPUT_FILE)

    # Spalten normalisieren
    df.columns = [
        "timestamp",
        "location",
        "air_temp",
        "snow_type",
        "snow_moisture",
        "wax_brand",
        "wax_product",
        "rating",
        "snow_temp",
        "layers"
    ]

    # Datentypen konvertieren
    df["air_temp"] = pd.to_numeric(df["air_temp"], errors="coerce")
    df["snow_temp"] = pd.to_numeric(df["snow_temp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("Int64")
    df["layers"] = pd.to_numeric(df["layers"], errors="coerce").astype("Int64")

    # Schneetyp vereinheitlichen
    mapping_snow_type = {
        "Neuschnee fein": "fresh_fine",
        "Neuschnee kalt": "fresh_cold",
        "Alt / umgewandelt": "old_transformed",
        "Eisig / gefroren": "icy",
        "Nassschnee": "wet",
        "Kunstschnee": "artificial",
        "Gemischt (Natur + Kunst)": "mixed"
    }
    df["snow_type"] = df["snow_type"].map(mapping_snow_type)

    # Schneefeuchte vereinheitlichen
    mapping_moisture = {
        "Trocken": "dry",
        "Normal": "normal",
        "Nass": "wet"
    }
    df["snow_moisture"] = df["snow_moisture"].map(mapping_moisture)

    # Standortnamen normalisieren
    df["location"] = df["location"].str.strip()

    # Fehlende Werte markieren
    df["snow_temp"] = df["snow_temp"].fillna(pd.NA)

    df.to_csv(OUTPUT_FILE, index=False)
    print("✔ Daten bereinigt und gespeichert als:", OUTPUT_FILE)

if __name__ == "__main__":
    clean_data()
