import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("reports/figures", exist_ok=True)

df = pd.read_csv("reports/results.csv")
anomalies = pd.read_csv("reports/anomalies.csv")

# Chart 1: normal vs anomalous traffic
df["status"].value_counts().plot(kind="bar")
plt.title("Normal vs Anomalous Traffic")
plt.xlabel("Status")
plt.ylabel("Number of Flows")
plt.tight_layout()
plt.savefig("reports/figures/normal_vs_anomalous_traffic.png")
plt.close()

# Chart 2: real dataset labels
if "Label" in df.columns:
    df["Label"].value_counts().plot(kind="bar")
    plt.title("Real Dataset Labels")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("reports/figures/real_labels.png")
    plt.close()

# Chart 3: most frequent destination ports in anomalies
if "Destination Port" in anomalies.columns:
    anomalies["Destination Port"].value_counts().head(10).plot(kind="bar")
    plt.title("Most Frequent Ports in Anomalies")
    plt.xlabel("Destination Port")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("reports/figures/anomalous_ports.png")
    plt.close()

print("Charts generated in reports/figures/")
