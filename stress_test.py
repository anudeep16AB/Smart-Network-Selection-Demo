import os
import requests
import time
import csv
import concurrent.futures
import pandas as pd

URL = "http://127.0.0.1:5000/api/recommend"
CONCURRENT_THREADS = 20

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "processed_data.csv")

print(f"Loading REAL capstone data from {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
    real_data_records = df.to_dict('records')
    TOTAL_REQUESTS = len(real_data_records)
    print(f"Successfully loaded {TOTAL_REQUESTS} real rows for full-scale testing.")
except Exception as e:
    print(f"ERROR: Could not load data. Details: {e}")
    exit()

def send_request(req_index):
    row = real_data_records[req_index]
    hour = int(row.get('Hour_of_Day', 12))
    
    payload = {
        "device_id": str(row.get("Device ID", f"D-{req_index}")),
        "current_carrier": str(row.get("Carrier", "AT&T")),
        "country_code": str(row.get("Country Code", "US")),
        "lat": str(row.get("Latitude", 40.71)),
        "lon": str(row.get("Longitude", -74.01)),
        "date": str(row.get("Date", "2026-09-27")),
        "time": f"{hour:02d}:00",
        "device_model": str(row.get("Device Metadata", "Unknown"))
    }
    
    start_time = time.time()
    try:
        response = requests.post(URL, data=payload, timeout=5)
        status = response.status_code
    except Exception:
        status = "FAILED"
        
    latency_ms = round((time.time() - start_time) * 1000, 2)
    return [req_index, status, latency_ms]

if __name__ == "__main__":
    print(f"Starting mass load test with {TOTAL_REQUESTS} requests...")
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        futures = [executor.submit(send_request, i) for i in range(TOTAL_REQUESTS)]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            results.append(future.result())
            if (i + 1) % 5000 == 0:
                print(f"Completed {i + 1}/{TOTAL_REQUESTS} requests...")

    csv_filename = "performance_logs.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Request_ID", "Status_Code", "Latency_ms"])
        writer.writerows(results)
        
    print(f"Mass load test complete. Hard analytical proof saved to {csv_filename}")