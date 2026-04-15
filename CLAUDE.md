# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

End-to-end e-commerce analytics pipeline: raw transactional Excel data → star schema CSV outputs → SQL analytics → Power BI dashboard.

## Pipeline Execution Order

Scripts must be run from the `python/` directory (paths are relative to it):

```bash
# Step 1 — convert raw Excel to CSV
cd python && python prepare_data.py

# Step 2 — build star schema (dimensions + fact table)
cd python && python build_star_schema.py
```

`prepare_data.py` reads `datasets/raw/online_retail.xlsx` and outputs `datasets/raw/orders.csv`.  
`build_star_schema.py` reads `datasets/raw/orders.csv` and writes 5 CSVs to `datasets/processed/`:  
`dim_products.csv`, `dim_customers.csv`, `dim_country.csv`, `dim_date.csv`, `fact_sales.csv`.

## Architecture

```
datasets/raw/online_retail.xlsx
        ↓  prepare_data.py
datasets/raw/orders.csv
        ↓  build_star_schema.py
datasets/processed/
  dim_products.csv   (product_id, stockcode, description)
  dim_customers.csv  (customer_id)
  dim_country.csv    (country_id, country)
  dim_date.csv       (date_id, date, year, month, day, weekday)
  fact_sales.csv     (invoice_no, product_id, customer_id, country_id, date_id, quantity, unit_price, revenue)
        ↓  Power BI
powerbi/ecommerceBI.pbix
```

The star schema uses surrogate keys (`product_id`, `country_id`, `date_id`) generated via `range()` — order-dependent, not stable across re-runs.

## Key Constraints

- **Raw and processed datasets are gitignored** — only `datasets/sample/` (small sample) is tracked. Do not commit large CSVs.
- All Python paths are relative to `python/` — run scripts from there, not from root.
- No test suite exists. Validation is done by inspecting output CSVs.
- `python/build_star_schema - copia.py` is a working copy/backup — treat as scratch file, not canonical.

## SQL Queries

`sql/business_queries.sql` contains 10 analytical queries designed for a SQL engine that has the star schema tables loaded (e.g. DuckDB, SQLite, or Power BI's DirectQuery). Queries assume table names: `fact_sales`, `dim_products`, `dim_customers`, `dim_country`, `dim_date`.

## Dependencies

Python: `pandas`, `openpyxl` (for Excel reading).

```bash
pip install pandas openpyxl
```
