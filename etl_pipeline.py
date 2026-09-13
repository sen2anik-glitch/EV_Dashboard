import requests
import pandas as pd

OUTPUT_FILE = "cleaned_ev_stations.csv"
BASE_URL = "https://data.wa.gov/resource/f6w7-q2d2.json"

print("Fetching data from Washington State Gov Open Data...")
response = requests.get(f"{BASE_URL}?$order=model_year DESC&$limit=1000")

print(f"Server response code: {response.status_code}")
data = response.json()
print(f"Successfully downloaded {len(data)} records.")

# Convert the raw data straight into a spreadsheet and save it
df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)
print("Spreadsheet created and saved successfully!")
