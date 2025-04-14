FROM python:3.11-slim

COPY ./requirements.txt .

RUN apt update && \
    apt install gcc -y && \
    pip install --upgrade pip && pip install -r requirements.txt && \
    rm requirements.txt

COPY ./flag.txt /root/
COPY ./getflag.c /
RUN gcc /getflag.c -o /getflag && \
    chmod u+s /getflag && \
    rm /getflag.c

WORKDIR /app
COPY ./src/ .
RUN useradd ctf && \
    chown -R ctf:ctf /app/flask_session/ && \
    chown -R ctf:ctf /app/user_files/  

USER ctf
EXPOSE 8000

ENTRYPOINT ["python3","app.py"]