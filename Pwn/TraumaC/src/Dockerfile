FROM debian:12

RUN apt update && \
    apt install -y socat gnustep-devel gdb && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --home-dir /home/trauma Trauma
WORKDIR /home/trauma

COPY ./trauma /home/trauma/trauma
COPY flag.txt /home/trauma/flag.txt

RUN chmod +x /home/trauma/trauma

EXPOSE 4444

USER Trauma


CMD socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/home/trauma/trauma,stderr
