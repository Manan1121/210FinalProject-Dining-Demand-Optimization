import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.model import load_and_merge_data, feature_engineering, train_models

st.title("Campus Dining Demand Optimization")
st.markdown("### CS210 Group Project: Darsh, Sanjana, Manan")

# Load Data & Train
with st.spinner('Training Models...'):
    df = load_and_merge_data()
    df_full, df_model = feature_engineering(df)
    results = train_models(df_model)

st.success("Models Trained Successfully!")

# Metric Display
col1, col2, col3 = st.columns(3)
col1.metric("Avg Traffic", int(df_full['traffic_count'].mean()))
col2.metric("Dataset Size", len(df_full))
col3.metric("RF MAE", round(results['Random Forest']['mae'], 2))

# Visualization
st.subheader("Actual vs Predicted Traffic (Random Forest)")

rf_result = results['Random Forest']
comparison_df = pd.DataFrame({
    'Actual': rf_result['y_test'],
    'Predicted': rf_result['preds']
}).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=comparison_df, x='Actual', y='Predicted', alpha=0.6)
plt.plot([0, 600], [0, 600], 'r--') # Perfect prediction line
plt.xlabel("Actual Traffic")
plt.ylabel("Predicted Traffic")
st.pyplot(fig)

st.subheader("Feature Importance")
rf_model = rf_result['model']
feat_imp = pd.DataFrame({
    'Feature': df_model.drop(columns=['traffic_count']).columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

st.bar_chart(feat_imp.set_index('Feature'))
