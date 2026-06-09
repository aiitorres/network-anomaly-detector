import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

# Load results
df = pd.read_csv("reports/results.csv")

# Convert real labels
# BENIGN = normal = 1
# Everything else = anomaly = -1
y_true = df["Label"].apply(lambda x: 1 if x == "BENIGN" else -1)

# Model prediction
y_pred = df["prediction"]

# Create confusion matrix and classification report
matrix = confusion_matrix(y_true, y_pred)
report = classification_report(y_true, y_pred)

print("Confusion matrix:")
print(matrix)

print("\nClassification report:")
print(report)

# Save metrics to a txt file
with open("reports/metrics.txt", "w", encoding="utf-8") as f:
    f.write("Confusion matrix:\n")
    f.write(str(matrix))
    f.write("\n\nClassification report:\n")
    f.write(report)

print("\nMetrics saved in reports/metrics.txt")
