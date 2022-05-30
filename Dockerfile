FROM python:3.9.13
RUN apt-get update 
COPY ./requirements.txt requirements.txt

RUN apt-get install -y snapd
RUN service snapd start
RUN systemctl start snapd.service
RUN snap install ngrok 
RUN install -r requirements.txt
EXPOSE 5002