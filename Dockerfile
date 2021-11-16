FROM python:3.9-bullseye

RUN pip3 install python-telegram-bot pythonping pyyaml BeautifulSoup4 pytelegrambotapi lxml mariadb

RUN mkdir /app

COPY ./BOT /app

WORKDIR /app

ENTRYPOINT ["python"]

CMD ["bot.py"] 
