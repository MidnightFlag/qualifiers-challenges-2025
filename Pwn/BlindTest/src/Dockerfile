FROM debian:12

RUN apt update &&\
apt install -y socat 

RUN apt-get update

RUN useradd --home-dir /home/blind_test --create-home blind_test 
RUN mkdir /home/blind_test/chall

COPY ./blind_test /home/blind_test/chall/
COPY flag.txt /home/blind_test/chall/
RUN chmod 555 /home/blind_test/chall/blind_test

WORKDIR /home/blind_test/chall
USER blind_test 

EXPOSE 4444

CMD socat tcp-listen:4444,reuseaddr,fork exec:/home/blind_test/chall/blind_test

