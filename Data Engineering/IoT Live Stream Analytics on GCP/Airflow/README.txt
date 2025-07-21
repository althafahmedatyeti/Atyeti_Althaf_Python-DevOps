# 🌀 Automated Dataproc Cluster Scheduler with Airflow

This project automates the **starting and stopping** of a Google Cloud **Dataproc cluster** using Apache Airflow.

## 📌 Overview

Managing Dataproc clusters efficiently can help save costs by turning them **off during idle times** and **starting them only when needed**. This project uses **Airflow DAGs** to automate this process.

---

## ⚙️ Tech Stack

- [x] Apache Airflow
- [x] Google Cloud Dataproc
- [x] Python
- [x] Google Cloud SDK

---

## 🗂️ Project Structure

```bash
airflow-dataproc-cluster-scheduler/
│
├── dags/
│   ├── start_cluster_dag.py   # DAG to start the cluster at 5:00 AM
│   └── stop_cluster_dag.py    # DAG to stop the cluster at 2:00 AM
│
├── README.md                  