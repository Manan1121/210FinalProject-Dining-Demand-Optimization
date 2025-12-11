import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.database import DB_PATH

def load_and_merge_data():
    conn = sqlite3.connect(DB_PATH)
    
    # Load raw tables
    traffic = pd.read_sql("SELECT * FROM traffic", conn)
    weather = pd.read_sql("SELECT * FROM weather", conn)
    events = pd.read_sql("SELECT * FROM events", conn)
    menu = pd.read_sql("SELECT * FROM menu", conn)
    
    conn.close()

    # Feature Engineering: Menu Stats [cite: 590]
    # Count vegetarian/vegan items per meal/hall
    menu['is_veg'] = menu['tags'].apply(lambda x: 1 if 'Vegetarian' in x else 0)
    menu_agg = menu.groupby(['date', 'meal_period', 'hall_name']).agg({
        'item_name': 'count',
        'is_veg': 'sum'
    }).rename(columns={'item_name': 'menu_items_count', 'is_veg': 'veg_items_count'}).reset_index()

    # Merge Traffic with Menu
    df = pd.merge(traffic, menu_agg, on=['date', 'meal_period', 'hall_name'], how='left')
    
    # Merge Weather
    df = pd.merge(df, weather, on=['date', 'meal_period'], how='left')
    
    # Merge Events (Logic: Left join on date and nearby_hall)
    events = events.rename(columns={'nearby_hall': 'hall_name'})
    df = pd.merge(df, events[['date', 'hall_name', 'expected_attendance']], 
                  on=['date', 'hall_name'], how='left')
    df['expected_attendance'] = df['expected_attendance'].fillna(0) # Fill no events with 0

    return df

def feature_engineering(df):
    # Time Features [cite: 598]
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # One-Hot Encoding for categorical [cite: 589]
    df = pd.get_dummies(df, columns=['meal_period', 'hall_name'], drop_first=True)
    
    # Drop non-numeric for modeling
    drop_cols = ['date', 'traffic_id', 'weather_id', 'event_id'] 
    df_model = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    return df, df_model

def train_models(df_model):
    X = df_model.drop(columns=['traffic_count'])
    y = df_model['traffic_count']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42)
    }
    
    results = {}
    
    print("\nModel Evaluation:")
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        
        results[name] = {"model": model, "mae": mae, "rmse": rmse, "preds": preds, "y_test": y_test}
        print(f"{name} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}")
        
    return results
