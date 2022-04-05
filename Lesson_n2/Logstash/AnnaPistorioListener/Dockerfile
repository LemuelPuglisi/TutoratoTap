FROM python:3.8.11-alpine3.14

WORKDIR /app

COPY . . 

RUN pip --no-cache-dir install -r requirements.txt

ENV PYTHONUNBUFFERED=0

EXPOSE 12000

CMD ["python", "-u", "aplistener.py"]