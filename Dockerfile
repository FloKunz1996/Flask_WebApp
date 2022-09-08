FROM python:3.9.13-slim

ENV APP_HOME=/app
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
	apt-get install -y gcc

COPY ./static ./static
COPY ./templates ./templates
COPY ./app.py .
COPY ./requirements.txt .
EXPOSE 7080
RUN pip install -r requirements.txt