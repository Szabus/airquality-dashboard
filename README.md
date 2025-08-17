## Using a .env file

You can store your API key in a `.env` file in the project root. Copy `.env.example` to `.env` and add your key:

```
cp .env.example .env
# Then edit .env and set your API key
```

The `.env` file is ignored by git, so your key will not be committed.

# OpenAQ API Key Setup

This project uses the OpenAQ v3 API, which requires an API key.

## How to get an API key

1. Register for a free API key at: https://docs.openaq.org/docs/getting-started
2. After registration, you will receive your API key.

## How to set the API key

Before running any scripts, set your API key as an environment variable named `OPENAQ_API_KEY`.

### On Windows (PowerShell):
```powershell
$env:OPENAQ_API_KEY = "your_api_key_here"
```

### On Linux/macOS (bash):
```bash
export OPENAQ_API_KEY="your_api_key_here"
```

Replace `your_api_key_here` with your actual API key.

Now you can run the scripts as described in the project.
# airquality-dashboard

AirQuality Dashboard is a simple and intuitive app that lets you monitor real-time air pollution levels and stay informed about the air you breathe.
