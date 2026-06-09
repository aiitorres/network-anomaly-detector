import pandas as pd
import numpy as np
import joblib
import os

# Create reports folder if it does not exist
os.makedirs("reports", exist_ok=True)

# Load model and columns
model = joblib.load("models/isolation_forest.joblib")
columns = joblib.load("models/columns.joblib")

# Load dataset
df = pd.read_csv("data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
df.columns = df.columns.str.strip()

# Use the same columns used during training
X = df[columns]

# Clean problematic values
X = X.replace([np.inf, -np.inf], np.nan)
X = X.dropna()

# Make predictions
predictions = model.predict(X)
scores = model.decision_function(X)

# Create results table
results = df.loc[X.index].copy()
results["prediction"] = predictions
results["anomaly_score"] = scores
results["status"] = results["prediction"].map({
    1: "Normal",
    -1: "Anomalous"
})

# Save full results
results.to_csv("reports/results.csv", index=False)

# Save only anomalies
anomalies = results[results["status"] == "Anomalous"]
anomalies.to_csv("reports/anomalies.csv", index=False)

print("Detection completed.")
print(f"Flows analyzed: {len(results)}")
print(f"Anomalies detected: {len(anomalies)}")
print("Generated files:")
print("- reports/results.csv")
print("- reports/anomalies.csv")
