FROM python:alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt \
	alembic upgrade head

CMD	["uvicorn main:app", "--reload", "--port", "8000"]