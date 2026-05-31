FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]