# NewsAPI Supply Chain Disruption ETL Pipeline

## Overview

This pipeline automates the collection, processing, and storage of real-time news articles related to global supply chain disruptions. It tracks 15 categories of supply chain risk events including port congestion, shipping delays, energy shocks, labor strikes, cyberattacks, and geopolitical conflicts that impact international trade.

Execution time is typically 150 seconds for a full run (depends on API response times and database write speed).

## What It Does

- **Extracts** news data from NewsAPI, a real-time news aggregation service
- **Transforms** raw article data by removing duplicates and cleaning entries
- **Loads** processed data into a PostgreSQL database and exports to CSV for analysis

The pipeline retrieves 15 distinct supply chain disruption categories:
1. Maritime chokepoints (Suez Canal, Panama Canal, Strait of Hormuz, etc.)
2. Port and container terminal operations
3. Global shipping and freight logistics
4. Energy sector disruptions (oil, gas, LNG, coal)
5. Semiconductor and electronics shortages
6. Manufacturing shutdowns
7. Trade policy and sanctions
8. Labor disputes and strikes
9. Transportation infrastructure failures
10. Weather and natural disasters
11. Financial system instability
12. Cyberattacks on logistics infrastructure
13. Pandemics and disease outbreaks
14. Agricultural and food supply shocks
15. Wars and conflicts affecting trade routes

## Technical Stack

- **Language**: Python 3
- **Data Processing**: pandas (data manipulation and cleaning)
- **Database**: PostgreSQL (persistent data storage)
- **Database Connector**: SQLAlchemy with psycopg2
- **API Integration**: NewsAPI Python client

## Key Features

- Queries 30 days of historical news data
- Deduplicates articles by URL to prevent redundant storage
- Handles API errors gracefully with error reporting
- Exports data to both CSV and PostgreSQL database for flexibility
- Progress tracking with `tqdm` visual indicators

## Database Output

Data is stored in the PostgreSQL table `newsapi_articles` with the following fields:
- Article title, description, and content
- Source URL and publication details
- Author and publication date
- Retrieval timestamp
