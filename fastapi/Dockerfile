FROM python:3.8.3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends netcat less gosu

RUN pip install poetry

COPY pyproject.toml* poetry.lock* ./

RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install; fi

COPY . .

ENTRYPOINT ["/src/entrypoint.sh"]