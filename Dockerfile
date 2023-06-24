FROM python:3.11.4-alpine
LABEL authors="kruase"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 server.py
