
import requests
import pandas as pd
import os
from dotenv import load_dotenv

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
	# Save all raw data to CSV
	df = pd.DataFrame([{k: v.get('v') for k, v in iaqi.items()}])
	out_path = os.path.join(os.path.dirname(__file__), "..", "data", f"waqi_{city.lower()}.csv")
	df.to_csv(out_path, index=False)
	print(f"Saved air quality data to {out_path}")
	return df

if __name__ == "__main__":
	fetch_waqi_city("Budapest")
