FROM debian:12

RUN apt update && \
    apt install -y gcc

RUN useradd --create-home --home-dir /home/neon_pulse Neon
WORKDIR /home/neon_pulse

COPY ./neonpulse /home/neon_pulse/neonpulse
COPY flag.txt /home/neon_pulse/flag.txt

RUN chmod +x /home/neon_pulse/neonpulse

USER Neon

EXPOSE 1337

COPY ./run.sh /home/neon_pulse/

ENTRYPOINT ["bash", "/home/neon_pulse/run.sh"]
