import logging
import json
import time


def log(chatID, action, level):
    user = "bot"
    if chatID == 0:
        user = "bot"
    else:
        user = str(chatID)

    data = {'level': logging.getLevelName(level), 'user': user, 'action': action, 'unixstamp': time.time()}
    logger = logging.getLogger('')
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    logger.info(json.dumps(data))
