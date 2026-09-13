import requests
import pandas as pd

OUTPUT_FILE = "cleaned_ev_stations.csv"
BASE_URL = "https://data.ny.gov/resource/bpkw-vkpj.json"

print("Fetching data from New York State Open Data...")
response = requests.get(f"{BASE_URL}?$limit=500")

print(f"Server response code: {response.status_code}")
data = response.json()
print(f"Successfully downloaded {len(data)} stations.")

# Convert the raw data straight into a spreadsheet and save it
df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)
print("Spreadsheet created and saved successfully!")
