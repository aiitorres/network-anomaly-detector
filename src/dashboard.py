import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Network Anomaly Detector",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Helper functions
# -----------------------------
def find_file(possible_paths):
    """
    Finds the first existing file from a list of possible paths.
    This allows the dashboard to work with English or Spanish filenames.
    """
    for path in possible_paths:
        if Path(path).exists():
            return path
    return None


@st.cache_data
def load_csv(path):
    """
    Loads a CSV file and caches it to improve dashboard speed.
    """
    return pd.read_csv(path)


def normalize_status(df):
    """
    Creates a clean status column using either:
    - the existing 'status' column
    - or the 'prediction' column from the Isolation Forest model
    """
    df = df.copy()

    if "status" in df.columns:
        status_map = {
            "normal": "Normal",
            "anómalo": "Anomalous",
            "anomalo": "Anomalous",
            "anomalous": "Anomalous"
        }

        df["status_clean"] = (
            df["status"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(status_map)
            .fillna(df["status"])
        )

    elif "prediction" in df.columns:
        df["status_clean"] = df["prediction"].map({
            1: "Normal",
            -1: "Anomalous"
        }).fillna("Unknown")

    else:
        df["status_clean"] = "Unknown"

    return df


# -----------------------------
# File paths
# -----------------------------
results_path = find_file([
    "reports/results.csv",
    "reports/resultados.csv"
])

anomalies_path = find_file([
    "reports/anomalies.csv",
    "reports/anomalias.csv"
])

metrics_path = find_file([
    "reports/metrics.txt",
    "reports/metricas.txt"
])

# -----------------------------
# Main title
# -----------------------------
st.title("Network Anomaly Detector")
st.caption("Dashboard for analyzing network traffic anomalies detected with Isolation Forest.")

# -----------------------------
# Validate files
# -----------------------------
if results_path is None:
    st.error("No results file was found. Run the detection script first.")
    st.code("python src/detect.py")
    st.stop()

# -----------------------------
# Load data
# -----------------------------
df = load_csv(results_path)
df.columns = df.columns.str.strip()
df = normalize_status(df)

if anomalies_path:
    anomalies = load_csv(anomalies_path)
    anomalies.columns = anomalies.columns.str.strip()
    anomalies = normalize_status(anomalies)
else:
    anomalies = df[df["status_clean"] == "Anomalous"].copy()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.title("Filters")

st.sidebar.write("Loaded files:")
st.sidebar.code(results_path)

if anomalies_path:
    st.sidebar.code(anomalies_path)

# Filter by status
status_options = sorted(df["status_clean"].dropna().unique())
selected_status = st.sidebar.multiselect(
    "Traffic status",
    status_options,
    default=status_options
)

filtered_df = df[df["status_clean"].isin(selected_status)]

# Filter by real label
if "Label" in df.columns:
    label_options = sorted(df["Label"].dropna().unique())
    selected_labels = st.sidebar.multiselect(
        "Real dataset label",
        label_options,
        default=label_options
    )

    filtered_df = filtered_df[filtered_df["Label"].isin(selected_labels)]

# Filter by destination port
if "Destination Port" in df.columns:
    port_options = sorted(df["Destination Port"].dropna().unique())

    selected_ports = st.sidebar.multiselect(
        "Destination port",
        port_options,
        default=[]
    )

    if selected_ports:
        filtered_df = filtered_df[filtered_df["Destination Port"].isin(selected_ports)]

# Filter by anomaly score
if "anomaly_score" in df.columns:
    min_score = float(df["anomaly_score"].min())
    max_score = float(df["anomaly_score"].max())

    selected_score_range = st.sidebar.slider(
        "Anomaly score range",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score)
    )

    filtered_df = filtered_df[
        (filtered_df["anomaly_score"] >= selected_score_range[0]) &
        (filtered_df["anomaly_score"] <= selected_score_range[1])
    ]

# -----------------------------
# Main metrics
# -----------------------------
total_flows = len(df)
total_anomalies = len(df[df["status_clean"] == "Anomalous"])
total_normal = len(df[df["status_clean"] == "Normal"])
anomaly_percentage = (total_anomalies / total_flows) * 100 if total_flows > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total flows", total_flows)
col2.metric("Normal flows", total_normal)
col3.metric("Anomalies", total_anomalies)
col4.metric("Anomaly percentage", f"{anomaly_percentage:.2f}%")

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Anomalies",
    "Ports and Labels",
    "Model Metrics",
    "Downloads"
])

# -----------------------------
# Tab 1: Overview
# -----------------------------
with tab1:
    st.subheader("General traffic overview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Traffic status distribution")
        status_counts = filtered_df["status_clean"].value_counts()
        st.bar_chart(status_counts)

    with col2:
        if "anomaly_score" in filtered_df.columns:
            st.write("Anomaly score distribution")

            score_distribution = pd.cut(
                filtered_df["anomaly_score"],
                bins=30
            ).value_counts().sort_index()

            score_distribution.index = score_distribution.index.astype(str)
            st.bar_chart(score_distribution)
        else:
            st.info("No anomaly_score column found.")

    st.divider()

    st.subheader("Filtered data preview")
    st.write(f"Rows after filters: {len(filtered_df)}")
    st.dataframe(filtered_df.head(200), use_container_width=True)

# -----------------------------
# Tab 2: Anomalies
# -----------------------------
with tab2:
    st.subheader("Detected anomalies")

    if len(anomalies) == 0:
        st.success("No anomalies were found.")
    else:
        st.write(f"Total detected anomalies: {len(anomalies)}")

        if "anomaly_score" in anomalies.columns:
            st.write("Most suspicious anomalies")
            most_suspicious = anomalies.sort_values(
                by="anomaly_score",
                ascending=True
            )
            st.dataframe(most_suspicious.head(100), use_container_width=True)
        else:
            st.dataframe(anomalies.head(100), use_container_width=True)

        st.divider()

        if "Destination Port" in anomalies.columns:
            st.subheader("Filter anomalies by destination port")

            anomaly_ports = sorted(anomalies["Destination Port"].dropna().unique())

            selected_anomaly_port = st.selectbox(
                "Select a destination port",
                anomaly_ports
            )

            anomalies_by_port = anomalies[
                anomalies["Destination Port"] == selected_anomaly_port
            ]

            st.write(
                f"Anomalies found for port {selected_anomaly_port}: "
                f"{len(anomalies_by_port)}"
            )

            st.dataframe(anomalies_by_port, use_container_width=True)

# -----------------------------
# Tab 3: Ports and Labels
# -----------------------------
with tab3:
    st.subheader("Ports and dataset labels")

    col1, col2 = st.columns(2)

    with col1:
        if "Destination Port" in anomalies.columns:
            st.write("Top 10 destination ports in anomalies")
            top_ports = anomalies["Destination Port"].value_counts().head(10)
            st.bar_chart(top_ports)
        else:
            st.info("No Destination Port column found.")

    with col2:
        if "Label" in df.columns:
            st.write("Real dataset labels")
            label_counts = df["Label"].value_counts().head(15)
            st.bar_chart(label_counts)
        else:
            st.info("No Label column found.")

    st.divider()

    if "Destination Port" in anomalies.columns:
        st.subheader("Anomaly port table")

        port_table = (
            anomalies["Destination Port"]
            .value_counts()
            .reset_index()
        )

        port_table.columns = ["Destination Port", "Anomaly Count"]

        st.dataframe(port_table, use_container_width=True)

# -----------------------------
# Tab 4: Model Metrics
# -----------------------------
with tab4:
    st.subheader("Model evaluation metrics")

    if metrics_path:
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = f.read()

        st.text(metrics)
    else:
        st.warning("No metrics file was found. Run the metrics script first.")
        st.code("python src/metrics.py")

    st.divider()

    st.info(
        "Reminder: Isolation Forest is an unsupervised model. "
        "The metrics compare the model output against the dataset labels, "
        "but the model was not trained directly with those labels."
    )

# -----------------------------
# Tab 5: Downloads
# -----------------------------
with tab5:
    st.subheader("Download generated reports")

    st.write("Download the full results or only the detected anomalies.")

    results_csv = df.to_csv(index=False).encode("utf-8")
    anomalies_csv = anomalies.to_csv(index=False).encode("utf-8")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download full results",
            data=results_csv,
            file_name="results.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            label="Download anomalies",
            data=anomalies_csv,
            file_name="anomalies.csv",
            mime="text/csv"
        )

    if metrics_path:
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics_text = f.read()

        st.download_button(
            label="Download model metrics",
            data=metrics_text,
            file_name="metrics.txt",
            mime="text/plain"
        )
