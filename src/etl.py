import pandas as pd
import sqlite3
import os
from src.database import DB_PATH, init_db

def run_etl(menu_df, traffic_df, weather_df, events_df):
    """
    Extracts data (from DFs), Transforms (cleans), and Loads into SQL.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    
    print("Starting ETL Process...")
    
    # Transformation: Date standardization [cite: 551]
    # (Already handled in generator, but ensuring format)
    for df in [menu_df, traffic_df, weather_df, events_df]:
        df['date'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m-%d")

    # Load into SQL 
    menu_df.to_sql('menu', conn, if_exists='replace', index=False)
    traffic_df.to_sql('traffic', conn, if_exists='replace', index=False)
    weather_df.to_sql('weather', conn, if_exists='replace', index=False)
    events_df.to_sql('events', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    print("ETL Completed. Data loaded into SQLite.")
