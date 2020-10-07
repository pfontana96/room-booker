FROM python:3.8

WORKDIR /room-booker

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x run.sh

EXPOSE 5000

ENTRYPOINT  ["./run.sh"]
