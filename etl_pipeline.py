import os
import requests
import pandas as pd
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
# It is highly recommended to get a free API key from https://developer.nrel.gov/signup/ 
# and set it as an environment variable (NREL_API_KEY).
API_KEY = os.getenv('NREL_API_KEY', 'DEMO_KEY')
BASE_URL = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json"
OUTPUT_FILE = "cleaned_ev_stations.csv"

def fetch_ev_stations_data():
    """Fetches electric vehicle station data from the NREL API."""
    logging.info("Starting data extraction from NREL API...")
    
    # We query for electric stations only
    params = {
        "api_key": API_KEY,
        "status": "E", # Open and Available
        "fuel_type": "ELEC", 
        "country": "US",
        "limit": 200 # For demo/prototyping purposes. Remove or paginate for full dataset.
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        stations = data.get('fuel_stations', [])
        logging.info(f"Successfully fetched {len(stations)} stations.")
        return stations
    else:
        logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        raise Exception("API Request Failed")

def transform_data(stations):
    """Cleans and structures the raw JSON data into a KPI-ready Pandas DataFrame."""
    logging.info("Transforming and cleaning data...")
    df = pd.DataFrame(stations)
    
    if df.empty:
        logging.warning("No data to transform.")
        return df

    # Select relevant columns for our KPIs
    cols_to_keep = [
        'id', 'station_name', 'city', 'state', 'zip', 
        'ev_network', 'open_date', 'ev_dc_fast_num', 'ev_level2_evse_num'
    ]
    df = df[[c for c in cols_to_keep if c in df.columns]]
    
    # Clean up Network Providers (impute missing)
    df['ev_network'] = df['ev_network'].fillna('Unknown/Independent')
    
    # Convert 'open_date' to datetime for YoY growth analysis
    df['open_date'] = pd.to_datetime(df['open_date'], errors='coerce')
    df['open_year'] = df['open_date'].dt.year
    
    # Ensure numeric types for charger counts and fill NaNs with 0
    df['ev_dc_fast_num'] = pd.to_numeric(df['ev_dc_fast_num'], errors='coerce').fillna(0)
    df['ev_level2_evse_num'] = pd.to_numeric(df['ev_level2_evse_num'], errors='coerce').fillna(0)
    df['total_chargers'] = df['ev_dc_fast_num'] + df['ev_level2_evse_num']
    
    logging.info("Data transformation complete.")
    return df

def main():
    try:
        raw_stations = fetch_ev_stations_data()
        clean_df = transform_data(raw_stations)
        
        if not clean_df.empty:
            clean_df.to_csv(OUTPUT_FILE, index=False)
            logging.info(f"Pipeline finished successfully. Data saved to {OUTPUT_FILE}")
        else:
            logging.warning("Pipeline finished but no data was saved.")
            
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
