import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
OUTPUT_FILE = "cleaned_ev_stations.csv"

def fetch_ev_stations_data():
    logging.info("Starting data extraction from NY State Government API...")
    
    # New York State Open Data: EV Charging Stations
    # NO API KEY REQUIRED! This bypasses all blocks.
    BASE_URL = "https://data.ny.gov/resource/bpkw-vkpj.json"
    
    response = requests.get(f"{BASE_URL}?$limit=500")
    
    if response.status_code == 200:
        data = response.json()
        logging.info(f"Successfully fetched {len(data)} stations from data.ny.gov.")
        return data
    else:
        logging.error(f"Failed to fetch data: {response.status_code}")
        raise Exception("API Request Failed")

def transform_data(stations):
    logging.info("Transforming and cleaning data...")
    df = pd.DataFrame(stations)
    if df.empty:
        return df

    # Keep relevant KPI columns
    cols_to_keep = ['station_name', 'city', 'state', 'zip', 'ev_network', 'ev_dc_fast_num', 'ev_level2_evse_num']
    df = df[[c for c in cols_to_keep if c in df.columns]]
    
    # Clean up missing data
    df['ev_network'] = df['ev_network'].fillna('Unknown')
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
    
