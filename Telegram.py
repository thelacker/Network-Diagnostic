import Serialisation
from telegram import Updater
import logging

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def status(bot, update):
    ip_dict = Serialisation.ip_dict_read()
    text = "Status:\n"
    for ip in ip_dict.items():
        if ip[1] == 0:
            text += "{0} is online\n".format(ip[0])
        if ip[1] == 1:
            text += "{0} is pre-online\n".format(ip[0])
        if ip[1] == 2:
            text += "{0} is pre-offline\n".format(ip[0])
        if ip[1] == 3:
            text += "{0} is offline\n".format(ip[0])
    bot.sendMessage(update.message.chat_id, text=text)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("158279031:AAFJxyWbRKs0yyglhvswN6DlPhUxp9fDqtc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("status", status)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()