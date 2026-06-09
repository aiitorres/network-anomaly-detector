import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 1. Load dataset
df = pd.read_csv("data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

# 2. Clean column names
df.columns = df.columns.str.strip()

# 3. Show labels
print("Labels found:")
print(df["Label"].value_counts())

# 4. Use only benign traffic for training
normal_df = df[df["Label"] == "BENIGN"].copy()

print(f"\nBenign flows used for training: {len(normal_df)}")

# 5. Select numeric columns
numeric_cols = normal_df.select_dtypes(include=["int64", "float64"]).columns

X_train = normal_df[numeric_cols]

# 6. Clean infinite and null values
X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_train = X_train.dropna()

# 7. Create model
model = Pipeline([
    ("scaler", StandardScaler()),
    ("detector", IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    ))
])

# 8. Train model
model.fit(X_train)

# 9. Save model
joblib.dump(model, "models/isolation_forest.joblib")

# 10. Save used columns
joblib.dump(list(numeric_cols), "models/columns.joblib")

print("\nModel trained successfully.")
print("Saved to models/isolation_forest.joblib")
