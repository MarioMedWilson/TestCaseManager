FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY config/ ./config/
COPY models/ ./models/
COPY routes/ ./routes/
COPY schemas/ ./schemas/
COPY utils/ ./utils/
COPY config/ ./config/
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
