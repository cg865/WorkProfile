FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py dbcontext.py person.py ./
COPY static/ static/
COPY templates/ templates/


EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
