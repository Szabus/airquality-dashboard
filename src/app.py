import os
import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def main():
    st.title("Air Quality Dashboard")

    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "waqi_data.db")
    if not os.path.exists(db_path):
        st.warning("No database found. Please run fetch_waqi.py first!")
        return
    conn = sqlite3.connect(db_path)
    # Get all cities in the database
    cities_query = "SELECT DISTINCT city FROM air_quality ORDER BY city"
    cities = [row[0].capitalize() for row in conn.execute(cities_query).fetchall()]
    if not cities:
        st.warning("No data found in the database. Please run fetch_waqi.py first!")
        conn.close()
        return
    selected_city = st.selectbox("Select a city:", cities)
    # Read all data for the selected city
    df = pd.read_sql_query(
        f"SELECT * FROM air_quality WHERE city = ? ORDER BY timestamp DESC",
        conn,
        params=(selected_city.lower(),),
    )
    conn.close()
    st.write(f"Data for {selected_city} (first 10 rows):")
    st.dataframe(df.head(10))

    st.subheader(f"Air quality values for {selected_city} (latest measurement)")
    if not df.empty:
        # Exclude city, timestamp, id columns from pollutants
        exclude_cols = {"city", "timestamp", "id"}
        values = {
            k: v for k, v in df.iloc[0].to_dict().items() if k not in exclude_cols
        }
        chart_df = pd.DataFrame(
            {"Pollutant": list(values.keys()), "Value": list(values.values())}
        )

        def color_picker(val):
            if val is None:
                return "#cccccc"
            try:
                v = float(val)
            except Exception:
                return "#cccccc"
            if v < 25:
                return "#4caf50"  # green
            elif v < 50:
                return "#ffeb3b"  # yellow
            elif v < 100:
                return "#ff9800"  # orange
            else:
                return "#f44336"  # red

        colors = [color_picker(v) for v in chart_df["Value"]]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=chart_df["Pollutant"], y=chart_df["Value"], marker_color=colors
                )
            ]
        )
        fig.update_layout(
            yaxis_title="Value", xaxis_title="Pollutant", showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
