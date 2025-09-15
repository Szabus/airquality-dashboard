
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from datetime import UTC
import sqlite3

def fetch_waqi_city(city="Budapest"):
	"""
	Fetch air quality data for a city from the World Air Quality Index (WAQI) API.
	Requires a WAQI API token in the WAQI_API_TOKEN environment variable.
	"""
	load_dotenv()
	token = os.environ.get("WAQI_API_TOKEN")
	if not token:
		raise RuntimeError("WAQI_API_TOKEN environment variable is not set. Please set your WAQI API token in a .env file or as an environment variable.")
	url = f"https://api.waqi.info/feed/{city}/?token={token}"
	response = requests.get(url)
	response.raise_for_status()
	data = response.json()
	if data.get("status") != "ok":
		print(f"No data found for city: {city}")
		return None
	iaqi = data["data"].get("iaqi", {})
	print(f"Air quality for {city}:")
	for k, v in iaqi.items():
		print(f"  {k}: {v.get('v')}")
	# Prepare new row with timestamp (timezone-aware)
	row = {k: v.get('v') for k, v in iaqi.items()}
	row['city'] = city
	row['timestamp'] = datetime.now(UTC).isoformat()
	db_path = os.path.join(os.path.dirname(__file__), "..", "data", "waqi_data.db")
	conn = sqlite3.connect(db_path)
	columns = list(row.keys())
	col_defs = ', '.join([f'"{col}" TEXT' for col in columns])
	create_table_sql = f"""
	CREATE TABLE IF NOT EXISTS air_quality (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		{col_defs}
	)
	"""
	conn.execute(create_table_sql)

	# Check for missing columns and add them if needed
	existing_cols = set()
	cursor = conn.execute("PRAGMA table_info(air_quality)")
	for row_info in cursor.fetchall():
		existing_cols.add(row_info[1])
	for col in columns:
		if col not in existing_cols:
			alter_sql = f'ALTER TABLE air_quality ADD COLUMN "{col}" TEXT'
			conn.execute(alter_sql)

	placeholders = ', '.join(['?'] * len(columns))
	insert_sql = f"INSERT INTO air_quality ({', '.join(columns)}) VALUES ({placeholders})"
	conn.execute(insert_sql, [str(row[col]) for col in columns])
	conn.commit()
	conn.close()
	print(f"Saved air quality data for {city} to {db_path}")
	return row


def fetch_waqi_cities(cities):
	"""
	Fetch and save air quality data for a list of cities.
	"""
	results = {}
	for city in cities:
		print(f"\nFetching data for {city}...")
		df = fetch_waqi_city(city)
		results[city] = df
	return results

if __name__ == "__main__":
	cities = ["Budapest", "Debrecen", "Szeged", "Gyor", "Pecs"]
	fetch_waqi_cities(cities)
