import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Pfad zur JSON Datei
CREDENTIALS_FILE = "credentials.json"

# Name der Google Tabelle 
SHEET_NAME = "Seefeld_Wax_Data"

def load_sheet():
    # Autorisierung
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    # Tabelle öffnen
    sheet = client.open(SHEET_NAME).worksheet("Formularantworten 1")

    # Daten in DataFrame laden
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":
    df = load_sheet()
    print("✔ Daten erfolgreich geladen!")
    print(df.head())

    # CSV exportieren
    df.to_csv("wax_data_seefeld.csv", index=False)
    print("✔ CSV gespeichert: wax_data_seefeld.csv")
