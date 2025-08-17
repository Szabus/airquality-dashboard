
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from fetch_waqi import fetch_waqi_city

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
