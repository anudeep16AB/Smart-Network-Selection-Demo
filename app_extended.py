import os
import sys
import logging
import pandas as pd
from flask import Flask, jsonify, render_template, request

# Configure standard output logging for Podman Desktop
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s] [PODMAN-LOG] [%(levelname)s] %(message)s'
)
logger = logging.getLogger("SmartNetworkApp")

app = Flask(__name__)

DATA_PATH = "fully_extended_processed_data.csv"

# Preload dataset into memory
df = None
if os.path.exists(DATA_PATH):
    try:
        logger.info(f"Loading dataset from: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        logger.info(f"Dataset loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
else:
    logger.warning(f"File {DATA_PATH} not found at container startup.")

@app.route('/')
def dashboard():
    logger.info("Serving interactive QoS dashboard UI.")
    return render_template('dashboard.html')

@app.route('/api/dataset-records', methods=['GET'])
def get_dataset_records():
    global df
    if df is not None:
        # Sample 100 rows across all columns for real-time presentation
        sample_df = df.sample(min(100, len(df)))
        records = sample_df.to_dict(orient='records')
        
        # Calculate summary metrics
        avg_signal = round(float(df['Signal_Reliability_Score'].mean()), 2) if 'Signal_Reliability_Score' in df else 0.0
        avg_reward = round(float(df['Composite_RL_Reward'].mean()), 2) if 'Composite_RL_Reward' in df else 0.0
        unique_carriers = int(df['Carrier'].nunique()) if 'Carrier' in df else 0

        logger.info(f"Transmitted 100 rows across {len(df.columns)} columns. Metrics computed.")
        return jsonify({
            "status": "success",
            "total_rows": len(df),
            "columns": list(df.columns),
            "metrics": {
                "avg_signal_reliability": avg_signal,
                "avg_composite_reward": avg_reward,
                "unique_carriers": unique_carriers
            },
            "data": records
        })
    
    logger.error("Dataset query requested but dataset is unavailable.")
    return jsonify({"status": "error", "message": "Extended dataset not found."}), 404

# NEW: Server-Side Database Query Endpoint
@app.route('/api/search', methods=['GET'])
def search_dataset():
    global df
    if df is not None:
        query = request.args.get('q', '').strip().lower()
        if not query:
            return jsonify({"status": "success", "data": []})
        
        # Searches across all columns for the query
        mask = df.astype(str).apply(lambda col: col.str.lower().str.contains(query)).any(axis=1)
        matched_df = df[mask].head(100) # Capped at 100 to keep UI fast
        
        records = matched_df.to_dict(orient='records')
        logger.info(f"DB Query: '{query}' returned {len(records)} matches.")
        return jsonify({
            "status": "success",
            "total_matches": len(matched_df),
            "data": records
        })
    return jsonify({"status": "error", "message": "Dataset unavailable."}), 404

@app.route('/api/extended-stats', methods=['GET'])
def get_extended_stats():
    global df
    if df is not None:
        sample_row = df.sample(1).to_dict(orient='records')[0]
        logger.info(f"Served legacy extended stats for Device ID: {sample_row.get('Device ID')}")
        return jsonify({
            "status": "success",
            "total_rows": len(df),
            "sample_extended_features": {
                "Mobility_State_Index": sample_row.get("Mobility_State_Index"),
                "App_Slicing_Profile": sample_row.get("App_Slicing_Profile"),
                "Battery_Drain_Rate_Pct": sample_row.get("Battery_Drain_Rate_Pct"),
                "Jitter_Loss_Percentage": sample_row.get("Jitter_Loss_Percentage"),
                "Composite_RL_Reward": sample_row.get("Composite_RL_Reward")
            }
        })
    return jsonify({"status": "error", "message": "Extended dataset not found."}), 404

if __name__ == '__main__':
    logger.info("Starting Flask Network Selection Engine on 0.0.0.0:5001")
    app.run(host='0.0.0.0', port=5001)