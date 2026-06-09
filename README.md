Network Anomaly Detector
========================

A basic network traffic anomaly detector using Python, pandas, scikit-learn, and Isolation Forest.

Objective
---------

Detect anomalous network flows based on numerical traffic features.

Dataset
-------

The CIC-IDS2017 dataset was used, specifically the CSV files prepared for machine learning.

Technologies
------------

*   Python
    
*   pandas
    
*   scikit-learn
    
*   Isolation Forest
    
*   Streamlit
    

How It Works
------------

1.  A CSV file containing network traffic is loaded.
    
2.  Benign traffic is filtered.
    
3.  An Isolation Forest model is trained.
    
4.  New network flows are analyzed.
    
5.  Result and anomaly files are generated.
    

Main Files
----------

*   src/train.py: trains the model.
    
*   src/detect.py: detects anomalies.
    
*   src/dashboard.py: displays visual results.
