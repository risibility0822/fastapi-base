# STAGE 1: 安裝套件、設置環境
FROM python:3.11-slim-buster as base

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# STAGE 2: 啟動服務
FROM python:3.11-slim-buster

WORKDIR /app

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /app

EXPOSE 8000

CMD uvicorn --host 0.0.0.0 --port 8000 main:app --proxy-headers