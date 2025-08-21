import tempfile
import shutil
from pathlib import Path
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from fetch_waqi import fetch_waqi_city, fetch_waqi_cities


@patch('fetch_waqi.fetch_waqi_city')
def test_fetch_waqi_cities_calls_city_fetch(mock_fetch_city):
	# Mock return value for each city
	mock_fetch_city.side_effect = lambda city: f"data_for_{city}"
	cities = ["Budapest", "Vienna", "Beijing"]
	results = fetch_waqi_cities(cities)
	# Check that fetch_waqi_city was called for each city
	assert mock_fetch_city.call_count == len(cities)
	for city in cities:
		assert results[city] == f"data_for_{city}"

 # Test: appending to CSV and checking for timestamp column
@patch('fetch_waqi.requests.get')
@patch('fetch_waqi.load_dotenv')
@patch.dict(os.environ, {"WAQI_API_TOKEN": "dummy_token"})
def test_fetch_waqi_city_appends_with_timestamp(mock_load_dotenv, mock_get):
	# Mock API response
	mock_response = MagicMock()
	mock_response.json.return_value = {
		"status": "ok",
		"data": {
			"iaqi": {
				"pm25": {"v": 10},
				"pm10": {"v": 20}
			}
		}
	}
	mock_response.raise_for_status = lambda: None
	mock_get.return_value = mock_response

	# Create a temporary directory for test data
	temp_dir = tempfile.mkdtemp()
	orig_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
	test_city = "Testcity"
	test_csv = os.path.join(temp_dir, f"waqi_{test_city.lower()}.csv")

	# Patch os.path.join to redirect data path to the temporary directory
	orig_join = os.path.join
	def fake_join(*args):
		if args[-2:] == ('data', f'waqi_{test_city.lower()}.csv'):
			return test_csv
		return orig_join(*args)

	with patch('os.path.join', side_effect=fake_join):
		# First call: should create a new file
		df1 = fetch_waqi_city(test_city)
		assert Path(test_csv).exists()
		df_loaded = pd.read_csv(test_csv)
		assert 'timestamp' in df_loaded.columns
		assert len(df_loaded) == 1
		# Second call: should append a new row
		df2 = fetch_waqi_city(test_city)
		df_loaded2 = pd.read_csv(test_csv)
		assert len(df_loaded2) == 2

	# Clean up the temporary directory
	shutil.rmtree(temp_dir)


@patch('fetch_waqi.requests.get')
@patch('fetch_waqi.load_dotenv')
@patch('builtins.print')
@patch.dict(os.environ, {"WAQI_API_TOKEN": "dummy_token"})
def test_fetch_waqi_city_no_data_print(mock_print, mock_load_dotenv, mock_get):
	mock_response = MagicMock()
	mock_response.json.return_value = {"status": "error"}
	mock_response.raise_for_status = lambda: None
	mock_get.return_value = mock_response
	result = fetch_waqi_city("Nowhere")
	assert result is None
	mock_print.assert_any_call("No data found for city: Nowhere")

@patch('fetch_waqi.load_dotenv')
def test_fetch_waqi_city_no_token(mock_load_dotenv):
	# Remove token if present
	if "WAQI_API_TOKEN" in os.environ:
		del os.environ["WAQI_API_TOKEN"]
	with pytest.raises(RuntimeError) as excinfo:
		fetch_waqi_city("Budapest")
	assert "WAQI_API_TOKEN environment variable is not set" in str(excinfo.value)

@patch('fetch_waqi.requests.get')
@patch('fetch_waqi.pd.DataFrame.to_csv')
@patch('fetch_waqi.load_dotenv')
@patch.dict(os.environ, {"WAQI_API_TOKEN": "dummy_token"})
def test_fetch_waqi_city_success(mock_load_dotenv, mock_to_csv, mock_get):
	# Mock API response
	mock_response = MagicMock()
	mock_response.json.return_value = {
		"status": "ok",
		"data": {
			"iaqi": {
				"pm25": {"v": 10},
				"pm10": {"v": 20}
			}
		}
	}
	mock_response.raise_for_status = lambda: None
	mock_get.return_value = mock_response

	df = fetch_waqi_city("Budapest")
	assert isinstance(df, pd.DataFrame)
	assert "pm25" in df.columns
	assert "pm10" in df.columns
	mock_to_csv.assert_called_once()

@patch('fetch_waqi.requests.get')
@patch('fetch_waqi.load_dotenv')
@patch.dict(os.environ, {"WAQI_API_TOKEN": "dummy_token"})
def test_fetch_waqi_city_no_data(mock_load_dotenv, mock_get):
	mock_response = MagicMock()
	mock_response.json.return_value = {"status": "error"}
	mock_response.raise_for_status = lambda: None
	mock_get.return_value = mock_response
	result = fetch_waqi_city("Nowhere")
	assert result is None
