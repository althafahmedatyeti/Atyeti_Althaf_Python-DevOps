### End-to-End Data Engineering Pipeline on Microsoft Azure
This project showcases the design and implementation of a robust, scalable, and production-grade data engineering pipeline using the Microsoft Azure ecosystem. The solution is built on a layered data lake architecture and demonstrates real-world data transformation and analytical capabilities using the AdventureWorks dataset.

✅ Project Overview
The pipeline follows a modular and scalable multi-layered architecture for data management and analytics:

🔹 Bronze Layer – Raw Ingestion:
Data was ingested from GitHub into Azure Data Lake using Azure Data Factory (ADF).

🔸 Silver Layer – Cleansing and Transformation:
Cleaned and semi-structured data was processed using Azure Databricks with PySpark.

🟡 Gold Layer – Aggregation and Modeling:
Final, curated datasets were transformed and modeled within Azure Synapse Analytics, ready for consumption.

📊 Visualization Layer – Insight Generation:
Power BI dashboards were developed for interactive and insightful data visualization, enabling actionable business decisions.

🛠️ Technologies & Tools Utilized
Component	Purpose
Azure Data Factory(Aznze),
Azure Databricks (PySpark),
Azure Synapse Analytics	Built analytical models, 
Azure Data Lake Storage Gen2	,
Power BI	Created dashboards to visualize KPIs and trends

📈 Project Outcome
This end-to-end solution delivers a scalable, secure, and modular data engineering pipeline on Azure, enabling enterprise-grade data processing and analytics. The curated data and Power BI dashboards provide stakeholders with real-time insights and decision support, demonstrating best practices in modern cloud-based data engineering.

