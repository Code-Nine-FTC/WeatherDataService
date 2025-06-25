FROM python:alpine

WORKDIR /app

COPY . .

RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

RUN mkdir -p /app/alembic/versions

RUN chmod -R 777 /app


CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--workers", "4"]
