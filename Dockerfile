FROM python:3.9-bullseye

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN mkdir -p ./bot-go/APP && \ 
    apt-get update && apt-get upgrade -y && \
    pip install poetry

WORKDIR /bot-go

COPY ./poetry.lock /bot-go
COPY ./poetry.toml /bot-go
COPY ./pyproject.toml /bot-go
COPY ./APP /bot-go/APP

RUN poetry config virtualenvs.create false --local && poetry update && poetry install

ENTRYPOINT ["python"]

CMD ["APP/bot.py"] 
