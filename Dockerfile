FROM python:alpine

WORKDIR /app

COPY . .

RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install -r requirements.txt 
RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--reload", "--port", "8000"]
