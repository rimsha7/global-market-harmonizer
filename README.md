# Global Market Harmonizer

## Overview

This project builds an end-to-end data engineering pipeline to harmonize global retail data into a single USD-based analytical view.

## Business Problem

Retail data exists in multiple currencies. Leadership requires a unified dashboard to:

* Track global revenue in USD
* Analyze product performance
* Understand exchange rate impact

---

## Architecture

### Phase 1: Data Extraction

* APIs:

  * Frankfurter (Exchange Rates)
  * Fake Store API (Product Metadata)
* Stored in AWS S3 (date-partitioned)

### Phase 2: Orchestration

* Apache Airflow DAG automates pipeline

### Phase 3: Data Processing

* Databricks (Silver Layer)
* Snowflake (Raw + Warehouse)

### Phase 4: Transformation (dbt)

* Star schema created
* Fact table: FACT_ORDERS
* Dimensions: Products, Exchange Rates

---

## Key Metric

Total Revenue (USD):

(Total USD) = (Local Price × Quantity) × Exchange Rate

---

## Phase 5: Governance

* Azure Purview used for:

  * Data lineage
  * Sensitive data classification

---

## Phase 6: Dashboard (Power BI)

Features:

* KPI cards (Revenue, Orders, AOV, Exchange Rate, YoY)
* Monthly revenue trend
* Revenue by category (Treemap)
* Exchange rate impact (Combo chart)
* Filters (Date, Category, Currency)
* Toggle (USD vs Local)

---

## Tools Used

* Python, Pandas, Boto3
* Airflow (Docker)
* Databricks
* Snowflake
* dbt
* Azure Purview
* Power BI

---

## Deliverables

* End-to-end pipeline
* Dashboard (.pbix)
* Lineage screenshot
* SQL validation queries

---

## Outcome

A scalable and automated data pipeline delivering a unified and business-ready analytics layer.
