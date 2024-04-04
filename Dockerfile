FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
ARG GIT_USERNAME
ARG GIT_PAT
RUN pip install poetry &&  \
    poetry config virtualenvs.create false &&  \
    poetry config repositories.git-iu-datamodels "https://github.com/Halone228/iu_datamodels" &&  \
    poetry config http-basic.git-iu-datamodels ${GIT_USERNAME} ${GIT_PAT} &&  \
    apt-get update && apt-get install git -y
RUN poetry install
ENTRYPOINT ["poetry", "run", "dev"]
