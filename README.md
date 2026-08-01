# NewsAPI Supply Chain Disruption ETL Pipeline

## Overview

This pipeline automates the collection, processing, and storage of real-time news articles related to global supply chain disruptions. It tracks 15 categories of supply chain risk events including port congestion, shipping delays, energy shocks, labor strikes, cyberattacks, and geopolitical conflicts that impact international trade.

## What It Does

1. **Extracts** news data from NewsAPI, a real-time news aggregation service
2. **Transforms** raw article data by removing duplicates and cleaning entries
3. **Loads** processed data into a PostgreSQL database and exports to CSV for analysis

The pipeline monitors 15 distinct supply chain disruption categories:
- Maritime chokepoints (Suez Canal, Panama Canal, Strait of Hormuz, etc.)
- Port and container terminal operations
- Global shipping and freight logistics
- Energy sector disruptions (oil, gas, LNG, coal)
- Semiconductor and electronics shortages
- Manufacturing shutdowns
- Trade policy and sanctions
- Labor disputes and strikes
- Transportation infrastructure failures
- Weather and natural disasters
- Financial system instability
- Cyberattacks on logistics infrastructure
- Pandemics and disease outbreaks
- Agricultural and food supply shocks
- Wars and conflicts affecting trade routes

## Technical Stack

- **Language**: Python 3
- **Data Processing**: pandas (data manipulation and cleaning)
- **Database**: PostgreSQL (persistent data storage)
- **Database Connector**: SQLAlchemy with psycopg2
- **API Integration**: NewsAPI Python client

## Key Features

- Queries 30 days of historical news data
- Retrieves up to 100 articles per query (Free API limitation)
- Deduplicates articles by URL to prevent redundant storage
- Handles API errors gracefully with error reporting
- Exports data to both CSV and SQL database for flexibility
- Progress tracking with visual indicators

## Use Cases

- Supply chain risk monitoring and alerting
- Predictive analytics for logistics disruptions
- Historical analysis of supply chain events
- Integration with business intelligence platforms
- Downstream Retrieval-Augmented Generation (RAG) pipelines

## Database Output

Data is stored in the PostgreSQL table `newsapi_articles` with the following fields:
- Article title, description, and content
- Source URL and publication details
- Author and publication date
- Retrieval timestamp

## Performance

Execution time: Typically 150 seconds for a full run (depends on API response times and database write speed).
