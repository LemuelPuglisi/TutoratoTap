FROM python:3.10.4-bullseye

WORKDIR /app

COPY . . 

RUN apt-get update

RUN apt-get install librdkafka-dev -y

RUN pip install --upgrade pip 

RUN pip --no-cache-dir install -r requirements.txt

ENV PYTHONUNBUFFERED=0

EXPOSE 5000

CMD ["python", "-u", "producer.py"]