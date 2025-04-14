FROM python:3.12-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/zandan-x.py /app/zandan-x.py
COPY src/flag.txt /app/flag.txt

EXPOSE 1337
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:'python3 /app/zandan-x.py',stderr,pty,raw,echo=0"]
