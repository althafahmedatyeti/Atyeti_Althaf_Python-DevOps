# 🚀 IoT Live Stream Data Pipeline with PySpark, BigQuery & Airflow

This project implements a **real-time data processing pipeline** for IoT sensor data using **PySpark** on **Google Cloud Platform (GCP)**. The pipeline ingests live data from simulated devices, detects anomalies and harmful gas emissions, and stores enriched output for further analysis.

---

## 🌍 Data Source

- Simulated IoT devices deployed across **Hyderabad city**
- Devices continuously send sensor readings in **JSON format** to **Google Cloud Pub/Sub**
- Monitored metrics:
  - `Temperature`
  - `Pressure`
  - `CO₂ levels`
  - `Harmful Gases` 

**Objective**: Monitor environmental health and detect hazardous conditions affecting public safety.

---

## 📦 Key Features

- 🔄 Real-time ingestion via **Cloud Pub/Sub**
- 🧠 Anomaly detection:
  - Constant/stuck `temperature` or `pressure`
- ☠️ Detection of **harmful gas emissions**
- ⚠️ Identification of system/device failure based on patterns
- 📤 Output destinations:
  - **Cloud Storage (GCS)** – backup of enriched data
  - **BigQuery** – for analytical dashboards

---

## 🛠️ Technologies Used

| Category            | Stack                               |
|---------------------|--------------------------------------|
| **Cloud Provider**  | Google Cloud Platform (GCP)         |
| **Streaming Engine**| Pub/Sub, PySpark Structured Streaming|
| **Compute**         | Dataproc Cluster                    |
| **Storage**         | Cloud Storage, BigQuery             |
| **Orchestration**   | Apache Airflow (Cloud Composer)     |
| **Language**        | Python                              |

---

## 🧠 Processing Logic (PySpark)

- Read from **Pub/Sub** using PySpark
- Perform transformations and apply logic:
  - Validate schema
  - Detect environmental anomalies
  - Classify system failures
- Write transformed stream to **GCS and BigQuery**

---

## 🎛️ Airflow Automation – Cluster Scheduling

To automate resource management and reduce costs, **Airflow DAGs** are used to start and stop the **Dataproc cluster** daily:

### ✅ `start_cluster_dag.py`
- ⏰ **Runs daily at 5:00 AM**
- 🚀 Starts the Dataproc cluster: `iot-processing-cluster`
- 🔧 Uses: `DataprocStartClusterOperator`

### 🛑 `stop_cluster_dag.py`
- ⏰ **Runs daily at 2:00 AM**
- 📴 Stops the cluster to avoid idle cost
- 🔧 Uses: `DataprocStopClusterOperator`

> Airflow ensures the cluster runs **only during the active streaming window**, making the pipeline cost-effective and production-ready.

---

## 📂 Project Structure

