import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

def main():
    st.title("Air Quality Dashboard")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    # Keressük meg az összes waqi_*.csv fájlt
    city_files = [f for f in os.listdir(data_dir) if f.startswith("waqi_") and f.endswith(".csv")]
    if not city_files:
        st.warning("No data files found. Please run fetch_waqi.py first!")
        return
    # Városok listája a fájlnevekből
    cities = [f.replace("waqi_", "").replace(".csv", "").capitalize() for f in city_files]
    city_to_file = {c: f for c, f in zip(cities, city_files)}
    selected_city = st.selectbox("Select a city:", cities)
    data_path = os.path.join(data_dir, city_to_file[selected_city])
    df = pd.read_csv(data_path)
    st.write(f"Data for {selected_city} (first 10 rows):")
    st.dataframe(df.head(10))

    st.subheader(f"Air quality values for {selected_city}")
    if not df.empty:
        values = df.iloc[0].to_dict()
        chart_df = pd.DataFrame({
            'Pollutant': list(values.keys()),
            'Value': list(values.values())
        })
        def color_picker(val):
            if val is None:
                return '#cccccc'
            try:
                v = float(val)
            except Exception:
                return '#cccccc'
            if v < 25:
                return '#4caf50'  # zöld
            elif v < 50:
                return '#ffeb3b'  # sárga
            elif v < 100:
                return '#ff9800'  # narancs
            else:
                return '#f44336'  # piros
        colors = [color_picker(v) for v in chart_df['Value']]
        fig = go.Figure(data=[go.Bar(
            x=chart_df['Pollutant'],
            y=chart_df['Value'],
            marker_color=colors
        )])
        fig.update_layout(yaxis_title='Value', xaxis_title='Pollutant', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
