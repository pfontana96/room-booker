FROM python:3.8

WORKDIR /room-booker

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python -m venv .venv
COPY requirements.txt requirements.txt
RUN .venv/bin/pip install -r requirements.txt
COPY . .
RUN chmod a+x boot.sh
EXPOSE 5000

ENTRYPOINT  ["./run.sh"]
