FROM python:3.12.2-slim
WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.create false
COPY pyproject.toml .
RUN poetry install

