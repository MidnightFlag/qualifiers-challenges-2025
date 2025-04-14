FROM alpine:latest

WORKDIR /app
COPY ./src /app

RUN apk update && apk add --no-cache \
    python3 \
    python3-dev \
    musl-dev \
    chromium \
    chromium-chromedriver \
    py3-pip \
    bash && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt

EXPOSE 80

CMD ["python3","/app/app.py"]