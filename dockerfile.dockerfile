FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y poppler-utils libsm6 libxext6 libxrender-dev libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]