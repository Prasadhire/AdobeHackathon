FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
