FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./dev

EXPOSE 8080

ENTRYPOINT ["sh", "dev/entrypoint_backend.sh"]
