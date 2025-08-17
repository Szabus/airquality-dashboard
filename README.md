
# airquality-dashboard

AirQuality Dashboard is a simple and intuitive Python app to monitor real-time air pollution levels in Budapest using the World Air Quality Index (WAQI) API. The project features automated data collection, a Streamlit dashboard, automated tests, and CI/CD with GitHub Actions.

## Features

- **Live air quality data** for Budapest from the WAQI API
- **Automated data fetch** and CSV export
- **Streamlit dashboard** for easy visualization
- **Unit tests** for data fetching logic (pytest)
- **CI/CD**: Automated testing and data update on every push/PR (GitHub Actions)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Szabus/airquality-dashboard.git
cd airquality-dashboard
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your WAQI API token

Register for a free API token at https://aqicn.org/data-platform/token/#/

You can store your token in a `.env` file in the project root:
```
WAQI_API_TOKEN=your_token_here
```
Or set it as an environment variable:
```powershell
$env:WAQI_API_TOKEN = "your_token_here"
```

### 5. Fetch air quality data
```bash
python src/fetch_waqi.py
```
This will save the latest data to `data/waqi_budapest.csv`.

### 6. Run the dashboard
```bash
streamlit run src/app.py
```


### 7. Run tests
```bash
pytest
```

### 8. Measure test coverage
Install coverage (ha még nincs):
```bash
pip install coverage
```
Futtasd a teszteket coverage-szel:
```bash
coverage run -m pytest
```
Jelentés a konzolra:
```bash
coverage report
```
HTML jelentés:
```bash
coverage html
```
Az eredmény a `htmlcov/index.html` fájlban böngészhető.

## CI/CD

GitHub Actions automatically runs tests and updates the data on every push and pull request for all branches. The WAQI API token must be set as a repository secret (`WAQI_API_TOKEN`) for CI to work.

## Project structure

- `src/fetch_waqi.py` – Fetches and saves air quality data from WAQI
- `src/app.py` – Streamlit dashboard
- `tests/test_fetch_waqi.py` – Unit tests for data fetching
- `requirements.txt` – Python dependencies
- `.github/workflows/python-app.yml` – CI/CD workflow

## License

MIT License
