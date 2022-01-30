FROM python:3.8.3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
