FROM ubuntu:24.04
RUN apt-get update && apt-get install -y \
    dumb-init \
    build-essential \
    git \
    vim \
    lsof \
    python3 \
    python3-dev \
    python3-pip && \
    apt-get clean

ADD src/requirements.txt /app/
RUN /usr/bin/python3 -m pip install -r /app/requirements.txt --break-system-packages
COPY src/ /app
WORKDIR /app
USER nobody
EXPOSE 8888
ENTRYPOINT ["/usr/local/bin/uwsgi", "--ini", "/app/uwsgi.ini"]
