### Import modules
import time
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone
from tqdm import tqdm
from sensitive_variables import username, password, db_name, NewsAPI_key


### Connect to PostgreSQL with username/password
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@localhost/{db_name}"
)
print("PostgreSQL database connected!")


# pandas_tables folder setup
out_folder = Path("pandas_tables")
out_folder.mkdir(exist_ok=True)


### ETL from NewsAPI
# Limited to 100 calls per day
from newsapi import NewsApiClient

start = time.perf_counter()

# API query setup
newsapi = NewsApiClient(api_key=NewsAPI_key)
queries = [
    # 1. Maritime chokepoints + critical canals/straits
    '("Suez Canal" OR "Panama Canal" OR "Strait of Hormuz" OR "Strait of Malacca" OR "Bab el-Mandeb" OR "Strait of Gibraltar" OR "Turkish Straits" OR Bosporus OR Dardanelles OR "Cape of Good Hope") AND (disruption OR blockage OR attack OR congestion OR delay OR closure)',
    # 2. Ports, terminals, and shipping infrastructure
    '(port OR "container terminal" OR harbor OR "container port" OR "shipping hub") AND (congestion OR backlog OR delay OR closure OR disruption OR "operational halt")',
    # 3. Global shipping + freight flow disruption
    '(shipping OR freight OR logistics OR "global trade" OR "ocean freight" OR "container shipping") AND (disruption OR delay OR shortage OR rerouting OR bottleneck OR imbalance)',
    # 4. Energy supply shocks (oil, gas, LNG, coal, nuclear fuel)
    '(oil OR crude OR petroleum OR LNG OR gas OR coal OR energy OR fuel) AND (spike OR shortage OR embargo OR sanctions OR disruption OR outage OR "price shock" OR "supply cut")',
    # 5. Semiconductor / electronics supply chain
    '(semiconductor OR chip OR "integrated circuit" OR electronics OR wafer OR fab OR foundry) AND (shortage OR disruption OR delay OR shutdown OR export restrictions)',
    # 6. Industrial production + manufacturing system shocks
    '(manufacturing OR factory OR production OR industrial OR assembly OR plant) AND (shutdown OR strike OR disruption OR shortage OR slowdown OR outage OR fire OR accident)',
    # 7. Trade policy / geopolitical restrictions
    '(tariffs OR sanctions OR embargo OR "export ban" OR "import restriction" OR "trade restriction" OR "technology restriction")',
    # 8. Labor + transport system disruption
    '(strike OR walkout OR "labor dispute" OR protest OR union OR strike action) AND (port OR railway OR trucking OR shipping OR logistics OR airline OR airport)',
    # 9. Transport infrastructure disruption (multi-modal)
    '(rail OR railway OR trucking OR highway OR "air cargo" OR aviation OR airport OR shipping OR port) AND (delay OR disruption OR congestion OR shutdown OR derailment OR accident OR closure)',
    # 10. Weather / climate / natural disaster impacts
    '(hurricane OR typhoon OR cyclone OR flood OR drought OR earthquake OR wildfire OR "extreme weather") AND ("supply chain" OR shipping OR port OR logistics OR factory OR production OR trade)',
    # 11. Financial system + macro instability transmission
    '(inflation OR recession OR "financial crisis" OR banking OR liquidity OR currency OR devaluation OR default OR debt) AND (global OR trade OR import OR export OR "supply chain")',
    # 12. Cyber + digital infrastructure disruption
    '(cyberattack OR ransomware OR outage OR "IT outage" OR "system failure") AND (port OR shipping OR logistics OR airline OR bank OR "payment system" OR "supply chain")',
    # 13. Health / pandemic / bio disruption
    '(pandemic OR epidemic OR outbreak OR disease OR quarantine) AND ("supply chain" OR logistics OR shipping OR manufacturing OR trade OR labor)',
    # 14. Commodity + food system shocks
    '(wheat OR rice OR corn OR soy OR fertilizer OR agriculture OR food OR grain) AND (shortage OR export ban OR disruption OR "price spike" OR "harvest failure")',
    # 15. Security / conflict impacts on trade routes
    '(war OR conflict OR invasion OR missile OR blockade OR insurgency OR piracy) AND (shipping OR "trade route" OR port OR logistics OR "supply chain" OR oil OR energy)'
]
days_ago = 30
from_date = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%Y-%m-%d")
all_articles = []

# Query the news and store to list of dictionaries
for q in tqdm(queries, desc="Retrieving NewsAPI..."):
    result = newsapi.get_everything(
        q=q,
        language="en",
        sort_by="relevancy",
        from_param=from_date,
        page_size=100,
        page=1
    )

    status = result.get("status")
    if status == 'ok':
        all_articles.extend(
            result.get("articles", [])
        )
    
    elif status == 'error':
        ErrorCode, ErrorMessage = result.get("code"), result.get("message")
        print(f'[01] Error {ErrorCode}: {ErrorMessage}')
        exit()

# Load into SQL
# Note that the if_exists="replace" is intentional for testing purposes
news_df = pd.DataFrame(all_articles)
news_df = news_df.dropna(subset=["url"])
news_df = news_df.drop_duplicates(subset="url")
news_df = news_df.drop(columns=["source",  "urlToImage"])

news_df.to_csv(out_folder / "news_df.csv", index=False)

news_df.to_sql(
    "newsapi_articles",
    engine,
    if_exists="replace",
    index=False,
    chunksize=1000,
    method="multi"
)

seconds_taken = time.perf_counter() - start
print(f"NewsAPI Supply Chain ETL complete! ({seconds_taken:.2f}s)")
