
FROM python:3.12-slim

WORKDIR /app

COPY ./app/req.txt /app/req.txt

RUN pip install --no-cache-dir -r req.txt \
    && pip install paho-mqtt


COPY ./app /app


EXPOSE 8000

RUN apt-get update && apt-get install -y mongodb-org \&& echo 'db.createCollection("readings")' 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
