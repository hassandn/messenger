FROM python:3.12.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY requirements.txt /code/

# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
