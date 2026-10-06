# Mamaearth Growth Analytics

## Project Overview

This project analyzes Mamaearth order data to identify revenue trends, return-rate patterns, data-quality issues, and high-risk customer segments.

The project is organized into three main stages:

1. SQL data pipeline
2. Python data cleaning and analysis
3. GenAI-powered business narrative

---

## 1. SQL Data Pipeline

The SQL layer uses SQLite to create and analyze the project database.

### Database Setup

From the project root:

```cmd
sqlite3 mamaearth_growth.db
```

Inside SQLite, load the database schema and seed data:

```sql
.read sql/schema.sql
.read sql/seed_data.sql
```

Run the SQL report:

```sql
.read sql/report.sql
```

The SQL layer works with the following tables:

* `customers`
* `product`
* `orders`

The SQL analysis covers customer activity, revenue, product categories, acquisition sources, and loyalty tiers.

> Note: The database included in this repository is already populated. The schema and seed commands are shown for rebuilding the database from scratch.

---

## 2. Python Data Cleaning, EDA and Visualizations

Run the data-cleaning and exploratory-analysis script:

```cmd
python analysis\clean_and_eda.py
```

The script:

* Loads the CSV files from the `data` folder
* Standardizes payment-method values
* Detects and removes duplicate orders
* Handles missing values
* Merges order, customer, and product data
* Calculates order values and revenue
* Detects quantity outliers
* Calculates return rates
* Calculates monthly revenue

Task 5 of Part 2 writes the verified findings to:

```text
narrator/findings.json
```

### Visualizations

Run:

```cmd
python analysis\visualize.py
```

The generated charts are saved in the `visualizations` folder:

* `return_rate_by_payment.png`
* `monthly_revenue_trend.png`

---

## 3. GenAI-Powered Insight Narrator

The narrator reads the verified findings from:

```text
narrator/findings.json
```

and generates an SCR (Situation-Complication-Resolution) business narrative.

### Gemini API

Install the Google GenAI package:

```cmd
pip install google-genai
```

Set the Gemini API key:

```cmd
set GEMINI_API_KEY=YOUR_API_KEY
```

Then run:

```cmd
python narrator\generate_narrative.py
```

The Gemini version uses a deterministic configuration and restricts numerical information in the narrative to the verified figures supplied in `findings.json`.

### Offline Fallback

The project also works without a Gemini API key.

Simply run:

```cmd
python narrator\generate_narrative.py
```

If `GEMINI_API_KEY` is not available, the program automatically uses the offline deterministic fallback.

The generated narrative contains:

* Situation
* Complication
* Resolution

and is saved to:

```text
narrator/sample_output.txt
```

The program also runs a numeric accuracy checklist to verify the required figures.

---

## Key Verified Findings

| Metric                              |        Result |
| ----------------------------------- | ------------: |
| Raw revenue                         | INR 99,860.20 |
| Cleaned revenue                     | INR 97,358.30 |
| Duplicate reconciliation difference |  INR 2,501.90 |
| COD return rate                     |         44.4% |
| CARD return rate                    |         14.7% |
| UPI return rate                     |         18.9% |
| Highest-risk segment                |  COD + Tier-2 |
| Highest-risk return rate            |         54.5% |
| True peak month                     |    March 2026 |
| True peak revenue                   | INR 20,318.90 |

---

## Project Structure

```text
mamaearth_growth.db

analysis/
├── clean_and_eda.py
└── visualize.py

data/
├── customers.csv
├── orders.csv
└── product.csv

narrator/
├── findings.json
├── generate_narrative.py
└── sample_output.txt

sql/
├── schema.sql
├── seed_data.sql
└── report.sql

visualizations/
├── return_rate_by_payment.png
└── monthly_revenue_trend.png

README.md
```

---

## Reproducibility

From the project root:

```cmd
python analysis\clean_and_eda.py
python analysis\visualize.py
python narrator\generate_narrative.py
```

The SQL database should be prepared before running the Python analysis when rebuilding the project database.

---

## Tools and Technologies

* SQLite
* SQL
* Python
* Pandas
* NumPy
* Matplotlib
* Google Gemini API
* Google GenAI Python SDK
* JSON
* GitHub
