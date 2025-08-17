import streamlit as st
import pandas as pd
import os

def main():
    st.title("Air Quality Dashboard (MVP)")
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waqi_budapest.csv")
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        st.write("Data (first 10 rows):")
        st.dataframe(df.head(10))
    else:
        st.warning("No data file found. Please run fetch_openaq.py first!")

if __name__ == "__main__":
    main()
