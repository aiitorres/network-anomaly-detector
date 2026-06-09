# Network Anomaly Detector

A basic network anomaly detection project built with Python, pandas, scikit-learn, Isolation Forest, and Streamlit.

The goal of this project is to analyze network flow data and identify anomalous behavior using machine learning. The model is trained with benign traffic and then used to detect flows that behave differently from normal network activity.

## Project Objective

The main objective of this project is to build a simple machine learning pipeline capable of detecting anomalous network traffic from CSV-based flow data.

This project was created as a beginner-friendly cybersecurity and machine learning project focused on:

* Network traffic analysis
* Anomaly detection
* Data preprocessing
* Machine learning model training
* Result visualization
* Dashboard creation

## Dataset

This project uses the CIC-IDS2017 dataset, specifically CSV files prepared for machine learning.

The dataset contains network flow features such as:

* Flow duration
* Total packets
* Packet length statistics
* Flow bytes per second
* Flow packets per second
* Destination port
* TCP flag counts
* Traffic labels

For the first version of the project, the model was trained using benign traffic and then tested against the complete dataset.

## Technologies Used

* Python
* pandas
* numpy
* scikit-learn
* Isolation Forest
* matplotlib
* joblib
* Streamlit
* Git and GitHub

## Project Structure

```text
network-anomaly-detector/
│
├── data/
│   └── raw/
│
├── models/
│   ├── isolation_forest.joblib
│   └── columns.joblib
│
├── reports/
│   ├── resultados.csv
│   ├── anomalias.csv
│   ├── metricas.txt
│   └── figures/
│
├── src/
│   ├── explore.py
│   ├── train.py
│   ├── detect.py
│   ├── metrics.py
│   ├── plots.py
│   ├── summary.py
│   └── dashboard.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

The project follows this pipeline:

```text
Dataset CSV
    ↓
Data cleaning
    ↓
Feature selection
    ↓
Model training with benign traffic
    ↓
Anomaly detection
    ↓
CSV reports
    ↓
Dashboard visualization
```

## Model

The project uses an Isolation Forest model.

Isolation Forest is an unsupervised machine learning algorithm commonly used for anomaly detection. It works by isolating unusual data points that behave differently from the majority of the dataset.

In this project:

* Benign traffic is used for training.
* The model learns the normal behavior of network flows.
* New or complete traffic data is analyzed.
* Flows are classified as normal or anomalous.

Prediction values:

```text
1  = Normal traffic
-1 = Anomalous traffic
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/network-anomaly-detector.git
cd network-anomaly-detector
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the project in this order:

```bash
python src/train.py
python src/detect.py
python src/metrics.py
python src/plots.py
python src/summary.py
streamlit run src/dashboard.py
```

## Main Scripts

| File               | Description                                     |
| ------------------ | ----------------------------------------------- |
| `src/explore.py`   | Explores the dataset columns, shape, and labels |
| `src/train.py`     | Trains the Isolation Forest model               |
| `src/detect.py`    | Detects anomalous network flows                 |
| `src/metrics.py`   | Generates evaluation metrics                    |
| `src/plots.py`     | Creates visual charts                           |
| `src/summary.py`   | Generates a text summary of the analysis        |
| `src/dashboard.py` | Launches the Streamlit dashboard                |

## Generated Outputs

After running the project, the following files are generated:

```text
reports/resultados.csv
reports/anomalias.csv
reports/metricas.txt
reports/resumen.txt
reports/figures/
```

The most important output files are:

| File             | Description                     |
| ---------------- | ------------------------------- |
| `resultados.csv` | Complete detection results      |
| `anomalias.csv`  | Only the anomalous flows        |
| `metricas.txt`   | Model evaluation metrics        |
| `resumen.txt`    | General summary of the analysis |
| `figures/`       | Generated charts                |

## Dashboard

The project includes a Streamlit dashboard that displays:

* Total analyzed flows
* Total detected anomalies
* Anomaly percentage
* Table of anomalous flows
* Filter by destination port
* Most frequent anomalous ports
* Real dataset labels
* Model metrics

To run the dashboard:

```bash
streamlit run src/dashboard.py
```

## Screenshots

### Main Dashboard

![Dashboard](screenshots/dashboard-main.png)

### Detected Anomalies

![Anomalies](screenshots/anomalies-table.png)

### Anomalous Ports

![Ports](screenshots/ports-chart.png)

## Results

The system generates anomaly detection results based on network flow behavior.

The model identifies suspicious or unusual flows by analyzing numerical traffic features. The final results are exported as CSV files and displayed through the dashboard.

Example results include:

* Number of analyzed flows
* Number of detected anomalies
* Percentage of anomalous traffic
* Most frequent destination ports in anomalous flows
* Classification metrics

## Limitations

This is a beginner-level project and has some limitations:

* It depends on the selected dataset.
* It does not analyze live traffic yet.
* It may generate false positives.
* It does not replace a professional IDS.
* The model currently uses only numerical features.
* Real-world deployment would require more testing and tuning.

## Future Improvements

Possible improvements for future versions:

* Analyze real network traffic with Zeek.
* Capture traffic using tcpdump.
* Compare multiple models such as Random Forest, One-Class SVM, or Local Outlier Factor.
* Add alert generation in JSON format.
* Improve the dashboard with more filters.
* Integrate the project with Suricata.
* Send alerts to Wazuh or another SIEM.
* Add Docker support.
* Add automatic model evaluation reports.

## What I Learned

Through this project, I practiced:

* Reading and cleaning network traffic datasets
* Working with CSV-based network flow data
* Training an anomaly detection model
* Using Isolation Forest for cybersecurity data
* Evaluating model results
* Creating reports with Python
* Building a basic dashboard with Streamlit
* Organizing a cybersecurity project for GitHub

## Disclaimer

This project is for educational and laboratory purposes only. It is designed to practice cybersecurity, data analysis, and machine learning concepts in a controlled environment.
