from src.generator import generate_data
from src.etl import run_etl
from src.model import load_and_merge_data, feature_engineering, train_models

def main():
    print("--- 1. Generating Simulated Data ---")
    menu, traffic, weather, events = generate_data()
    
    print("\n--- 2. Running ETL Pipeline ---")
    run_etl(menu, traffic, weather, events)
    
    print("\n--- 3. Merging & Feature Engineering ---")
    df = load_and_merge_data()
    print(f"Merged Dataset Shape: {df.shape}")
    
    df_full, df_model = feature_engineering(df)
    
    print("\n--- 4. Training & Evaluating Models ---")
    results = train_models(df_model)
    
    print("\nSuccess! System is ready for visualization.")

if __name__ == "__main__":
    main()
