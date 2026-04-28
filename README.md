# 🌍 Global Market Harmonizer

A cloud-native data engineering pipeline that transforms multi-currency retail data into a unified USD-based analytics system.

---

## 🚀 Overview

This project solves the challenge of fragmented global retail data stored in multiple currencies by building an end-to-end pipeline that:

* Extracts external data (exchange rates & product metadata)
* Processes and standardizes data
* Converts all revenue into USD
* Provides an interactive dashboard for business insights

---

## 🏗️ Architecture

```
APIs → S3 → Airflow → Databricks → Snowflake → dbt → Power BI
```

---

## ⚙️ Tech Stack

| Tool           | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Data extraction                    |
| AWS S3         | Data lake storage                  |
| Apache Airflow | Workflow orchestration             |
| Databricks     | Data transformation (Silver Layer) |
| Snowflake      | Data warehouse (Gold Layer)        |
| dbt            | Data modeling & testing            |
| Azure Purview  | Data governance & lineage          |
| Power BI       | Data visualization                 |

---

## 🔄 Data Pipeline

### 1. Data Ingestion

- Frankfurter API → Exchange Rates
- Fake Store API → Product Metadata

### 2. Orchestration

- Automated using Apache Airflow DAG

### 3. Processing

- Databricks used for cleaning and transformation

### 4. Storage

- Snowflake stores structured data

### 5. Transformation

- dbt creates star schema (Fact + Dimensions)

---

## 🖼️ Dashboard Preview

![Dashboard](screenshots/report.png)

---

## ⚙️ Environment Setup

### Requirements

* Python 3.11+
* Docker & Docker Compose
* Apache Airflow (Dockerized)
* dbt (Snowflake adapter)
* Snowflake account
* Databricks workspace
* Power BI Desktop

---

### Python Setup

```bash
python -m venv .venv
```

Activate environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧪 Versions

| Tool              | Version |
| ----------------- | ------- |
| Python            | 3.11    |
| dbt               | 1.11.8  |
| Snowflake Adapter | 1.11.4  |
| Apache Airflow    | 2.9.1   |
| Docker            | Latest  |
| Power BI          | Latest  |

---

## 🔐 Environment Variables

Create a `.env` file:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
```

## ▶️ Running the Project

### Step 1: Run Data Extraction

```bash
python -m extraction.main
```

This will:

* Fetch API data
* Upload to AWS S3

---

### Step 2: Start Airflow

```bash
docker compose -f airflow/docker-compose.yaml up -d
```

Open Airflow UI:

```
http://localhost:8080
```

Trigger DAG:

```
global_market_ingestion
```

---

### Step 3: Run dbt Models

```bash
cd retail_dbt
dbt run
dbt test
```

---

### Step 4: View Dashboard

Open Power BI file:

```
powerbi/Global_Market_Harmonizer.pbix
```

---

## 🧪 Data Validation

```sql
SELECT COUNT(*) FROM retail_db.raw.internal_orders;
SELECT COUNT(*) FROM analytics.fact_orders;
```

---

## 🔐 Data Governance

* Azure Purview used for:

  - Data lineage tracking
  - Sensitive data classification

---

## 📌 Conclusion

This project demonstrates a scalable and automated approach to global data harmonization, enabling better decision-making through unified analytics.

---

## 🌐 Author

Made by  
[![GitHub](https://img.shields.io/badge/GitHub-rimsha7-181717?logo=github&logoColor=white)](https://github.com/rimsha7)

---
