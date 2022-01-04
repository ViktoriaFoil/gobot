FROM python:3.9-bullseye

RUN mkdir -p ./bot-go/BOT && \ 
    apt-get update && apt-get upgrade -y && \
    pip install poetry

WORKDIR /bot-go


COPY ./poetry.lock /bot-go
COPY ./poetry.toml /bot-go
COPY ./pyproject.toml /bot-go
COPY ./BOT /bot-go/BOT

RUN poetry config virtualenvs.create false --local && poetry update && poetry install

ENTRYPOINT ["python"]

CMD ["BOT/bot.py"] 
