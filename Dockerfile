FROM python:3.9-slim

ARG DEBIAN_FRONTEND=noninteractive

COPY ./Sources/ /opt/shadowroller/Sources
COPY ./Ressources/ /opt/shadowroller/Ressources
RUN python3 -m pip install -U discord.py numpy


WORKDIR /opt/shadowroller/Sources/
CMD python3 main.py