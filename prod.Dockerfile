FROM python:3.12-slim-bookworm
WORKDIR /app
COPY . .
ARG GIT_USERNAME
ARG GIT_PAT
HEALTHCHECK --interval=10s --timeout=20s --retries=1 CMD curl -sS http://127.0.0.1:9788/healthy || exit 1
RUN pip install poetry && apt update -y && apt install libpq-dev -y && \
    poetry config virtualenvs.create false && \
    poetry config repositories.git-iu-datamodels "https://github.com/Halone228/iu_datamodels" &&  \
    poetry config http-basic.git-iu-datamodels ${GIT_USERNAME} ${GIT_PAT} &&  \
    apt-get update && apt-get install git -y
RUN poetry install
ENTRYPOINT ["poetry", "run", "dev"]
