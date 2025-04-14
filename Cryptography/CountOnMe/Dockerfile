FROM python:3.9-slim

RUN apt-get update && apt-get install -y socat

WORKDIR /chall

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 1337

CMD socat tcp-l:1337,reuseaddr,fork exec:"python /chall/app.py"