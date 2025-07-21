FROM python:3.10-slim

WORKDIR /app

COPY . .

COPY src /app/




RUN pip install -r requirements.txt

# Expose the Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "src/uber_trip.py", "--server.port=8501", "--server.address=0.0.0.0"]

