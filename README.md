

==============================================================================
README==============================================================================

# Campus Dining Demand Optimization

## Project Overview
This project is a data-driven forecasting system designed to predict student foot traffic at university dining halls. By integrating menu offerings, weather conditions, campus events, and simulated traffic data, the system optimizes food preparation to reduce waste and wait times.

The solution features a full ETL pipeline, a normalized SQL database, and Machine Learning models (Random Forest, Gradient Boosting) that achieve ~95% prediction accuracy.

## Features
* Data Pipeline: Automates the generation and cleaning of menu, traffic, weather, and event data.
* SQL Database: Stores normalized data in SQLite for complex querying.
* Machine Learning: Trains Linear Regression, Random Forest, and Gradient Boosting models.
* Interactive Dashboard: A Streamlit web app to visualize traffic predictions and feature importance.

## Folder Structure
Dining_Demand_Optimization/
├── data/                   # Stores generated CSVs and the SQLite database
├── src/
│   ├── __init__.py
│   ├── database.py         # Defines SQL schema and connection
│   ├── generator.py        # Simulates traffic/menu/weather data
│   ├── etl.py              # Loads cleaned data into the DB
│   └── model.py            # Feature engineering and model training
├── app.py                  # Streamlit Dashboard (Frontend)
├── main.py                 # Master script to run ETL and Model training
└── requirements.txt        # Project dependencies

## Setup & Installation

1. Prerequisites
Ensure you have Python 3.8+ installed.

2. Install Dependencies
Open your terminal/command prompt in the project folder and run:
pip install -r requirements.txt

## How to Run

Step 1: Initialize Database & Train Models
Run the backend script to generate the simulated data, populate the SQL database, and train the machine learning models.
python main.py

Output: You will see logs indicating data generation, ETL completion, and model evaluation metrics (MAE/RMSE) in the console.

Step 2: Launch the Dashboard
Start the interactive visualization tool to explore the results.
streamlit run app.py

Output: This will automatically open a tab in your web browser (usually at http://localhost:8501) displaying the Actual vs. Predicted graphs and Feature Importance charts.

## Key Results
* Best Model: Gradient Boosting Regressor
* Mean Absolute Error (MAE): ~13.80
* Accuracy: ~95% (approx. 5.35% error rate)
* Primary Driver: Time of Day (Lunch/Dinner) is the strongest predictor of student traffic.

## Authors
CS 210 Group Project
* Darsh Sundar: Database Design & SQL
* Sanjana Nuti: Data Simulation & ETL
* Manan Shah: Machine Learning & Visualization