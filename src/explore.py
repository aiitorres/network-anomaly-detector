import pandas as pd

# Load the CSV file
df = pd.read_csv("data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Show the number of rows and columns
print("Rows and columns:")
print(df.shape)

# Show the first rows of the dataset
print("\nFirst rows:")
print(df.head())

# Show column names
print("\nColumns:")
print(df.columns)

# Show label counts
print("\nLabels:")
print(df["Label"].value_counts())
