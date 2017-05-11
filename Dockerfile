FROM python:3-alpine

WORKDIR /app
COPY requirements.txt /app

RUN apk --no-cache add --virtual=.build-deps gcc build-base musl-dev &&\
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY . /app

VOLUME /app/data
CMD ["python", "app.py"]
