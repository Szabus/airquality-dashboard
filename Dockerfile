# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/
COPY data/ ./data/

# Expose Streamlit's default port
EXPOSE 8501

# Set environment variable for Streamlit (optional, disables telemetry)
ENV STREAMLIT_TELEMETRY="0"

# Default command: run the Streamlit dashboard
CMD ["streamlit", "run", "src/app.py"]
