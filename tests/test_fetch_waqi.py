import os
import shutil
import sqlite3
import sys
import tempfile
from unittest.mock import MagicMock, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from fetch_waqi import fetch_waqi_cities


import os
import shutil
import sqlite3
import sys
import tempfile
from unittest.mock import MagicMock, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from fetch_waqi import fetch_waqi_cities


@patch("fetch_waqi.requests.get")
@patch("fetch_waqi.load_dotenv")
@patch.dict(os.environ, {"WAQI_API_TOKEN": "dummy_token"})
def test_fetch_waqi_city_sqlite_insert_and_column_add(mock_load_dotenv, mock_get):
    # Mock API response with two pollutants
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "ok",
        "data": {"iaqi": {"pm25": {"v": 10}, "pm10": {"v": 20}}},
    }
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    # Use a temporary directory for the database
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "waqi_data.db")

    # Patch os.path.join to redirect database path
    orig_join = os.path.join

    def fake_join(*args):
        if args[-2:] == ("data", "waqi_data.db"):
            return db_path
        return orig_join(*args)

    with patch("os.path.join", side_effect=fake_join):
        from fetch_waqi import fetch_waqi_city

        fetch_waqi_city("Testcity")
        # Check that the row is inserted
        conn = sqlite3.connect(db_path)
        cur = conn.execute("SELECT city, pm25, pm10 FROM air_quality")
        row = cur.fetchone()
        assert row[0] == "Testcity"
        assert row[1] == "10"
        assert row[2] == "20"
        # Now mock a new pollutant
        mock_response.json.return_value["data"]["iaqi"]["dew"] = {"v": 5}
        fetch_waqi_city("Testcity")
        # Check that the new column exists
        cur = conn.execute("PRAGMA table_info(air_quality)")
        columns = [r[1] for r in cur.fetchall()]
        assert "dew" in columns
        conn.close()

    shutil.rmtree(temp_dir)


@patch("fetch_waqi.fetch_waqi_city")
def test_fetch_waqi_cities_calls_city_fetch(mock_fetch_city):
    # Mock return value for each city
    mock_fetch_city.side_effect = lambda city: f"data_for_{city}"
    cities = ["Budapest", "Vienna", "Beijing"]
    results = fetch_waqi_cities(cities)
    # Check that fetch_waqi_city was called for each city
    assert mock_fetch_city.call_count == len(cities)
    for city in cities:
        assert results[city] == f"data_for_{city}"
