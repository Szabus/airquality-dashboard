

# airquality-dashboard

AirQuality Dashboard is a Python-based application that collects air quality data for multiple cities using the World Air Quality Index (WAQI) API and displays it on a Streamlit dashboard. Data is stored in an SQLite database, collection is automated (GitHub Actions), the project is tested, and can be run with Docker.


## Main Features

- **Collect air quality data for multiple cities** (WAQI API)
- **Automated data collection** once daily (7:00 UTC) via GitHub Actions
- **SQLite database** (`data/waqi_data.db`) for storing measurements
- **Streamlit dashboard**: city selection, colored bar charts, time series trends
	- Compare multiple cities (if enabled)
	- Download/export data (if enabled)
	- Alerts/notifications (optional, if implemented)
- **Unit tests** (pytest)
- **CI/CD**: automated testing and data updates
- **Code scanning**: CodeQL workflow for security/code quality (see Security tab on GitHub)
- **Docker support**

## Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/Szabus/airquality-dashboard.git
cd airquality-dashboard
```

### 2. Create a virtual environment (optional)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your WAQI API token

Register for a free API token: https://aqicn.org/data-platform/token/#/

Set it as an environment variable (e.g. in `.env` or your shell):
```powershell
$env:WAQI_API_TOKEN = "your_token_here"
```

### 5. Manually fetch air quality data
```bash
python src/fetch_waqi.py
```
Data will be saved to the `data/waqi_data.db` SQLite database.

### 6. Run the dashboard
```bash
streamlit run src/app.py
```
Select a city and view air quality data on colorful charts!

### 7. Run tests
```bash
pytest
```

### 8. Measure test coverage
```bash
pip install coverage
coverage run -m pytest
coverage report
coverage html
```
Results are viewable in `htmlcov/index.html`.

### 9. Using Docker
If a `Dockerfile` is present, build and run:
```bash
docker build -t airquality-dashboard .
docker run -p 8501:8501 airquality-dashboard
```


## Automated Data Collection (GitHub Actions)

The `.github/workflows/scheduled-fetch.yml` workflow runs automatically once a day (7:00 UTC), updates the database, and commits changes. The WAQI API token must be set as a repo secret (`WAQI_API_TOKEN`).

## Code Scanning & Security

CodeQL analysis is enabled via GitHub Actions. Results and alerts can be viewed under the repository's **Security** → **Code scanning alerts** tab. This helps identify potential security and code quality issues automatically.

## Project Structure

- `src/fetch_waqi.py` – Data collection, SQLite handling, multi-city support
- `src/app.py` – Streamlit dashboard, city selection, visualization
- `data/waqi_data.db` – SQLite database with measurements
- `tests/test_fetch_waqi.py` – Unit tests
- `requirements.txt` – Python dependencies
- `.github/workflows/scheduled-fetch.yml` – Automated data collection workflow
- `Dockerfile` – (optional) Docker support

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.

## License

MIT License
