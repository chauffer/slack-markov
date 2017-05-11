FROM python:3-alpine

WORKDIR /app
COPY requirements.txt /app

RUN apk --no-cache --virtual=.build-deps add build-base musl-dev git &&\
    mkdir -p /dependencies && cd /dependencies &&\
    pip install --no-cache-dir -r /app/requirements.txt &&\
    apk --purge del .build-deps

COPY . /app

VOLUME /app/data
CMD ["python", "app.py"]
