FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install 
ENTRYPOINT ["poetry", "run", "dev"]