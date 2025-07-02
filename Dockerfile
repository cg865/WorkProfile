FROM python:3.9-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --target=/python-packages -r requirements.txt


FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /python-packages /usr/local/lib/python3.9/site-packages

COPY app.py dbcontext.py person.py ./
COPY static/ static/
COPY templates/ templates/

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
