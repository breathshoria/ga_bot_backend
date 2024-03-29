import logging
import os
import random
import sys

from telegram.ext import Updater, CommandHandler

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        updater.idle()
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(update, context):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.\
        reply_text("Привет!\nЭто твой chat_id - {} \n"
                   "Ниже будут оповещения, напши /help для более подробной информации".format(update.message.chat.id))

def help_handler(update, context):
    # Creating a handler-function for /start command
    logger.info("User {} started helper".format(update.effective_user["id"]))
    update.message.\
        reply_text("Отправь chat_id")




if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    run(updater)