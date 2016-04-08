import Serialisation
from telegram import Updater
import logging
import Diagnostic
import pickle

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

constructions = {'10.10.4.24': 'Avtozavodskaya', '10.10.4.7': 'Bryanski post',
                 '10.10.4.11': 'Butyrski', '10.10.4.23': 'Domodedovo',
                 '10.10.4.9': 'Entuziastov', '10.10.4.14': 'Kashirskoe',
                 '10.10.4.6': 'Kutuzovski', '10.10.4.17': 'Leningradski A/B',
                 '10.10.4.20': 'Mira A/B', '10.10.4.25': 'Rusakovskaya',
                 '10.10.4.5': 'Trofimova', '10.10.4.10': 'Sokolniki',
                 '10.10.4.12': 'Varshavskoe', '10.10.4.21': 'Varshavskoe obl',
                 '10.10.4.15': 'Volgogradski', '10.10.4.13': 'Volokolamskaya',
                 '10.10.4.8': 'Yaroslavskoe', '10.10.4.19': 'Zvenigorodskoe',
                 "10.10.5.230": "sftp", "bot": None, "update": list()}


def get_constructions():
    with open('data.pickle', 'rb') as f:
        constructions = pickle.load(f)

    return constructions


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    constructions = get_constructions()
    newupdate = constructions["update"]
    newupdate.append(update.message.chat_id)
    constructions.update({"bot": bot, "update": newupdate})
    with open('data.pickle', 'wb') as f:
        pickle.dump(constructions, f)
    bot.sendMessage(update.message.chat_id, text='Hello!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def status(bot, update):
    ip_dict = Serialisation.ip_dict_read()
    ip_dict.sort()
    text = "Status:\n"
    text_pre_of = ''
    text_pre_on = ''
    text_of = ''
    for ip in ip_dict.items():
        if ip[1][0] == 0:
            text += "{0} is online\n".format(constructions[str(ip[0])])
        if ip[1][0] == 1:
            text_pre_on += "{0} is pre-online\n".format(constructions[str(ip[0])])
        if ip[1][0] == 2:
            text_pre_of += "{0} is pre-offline\n".format(constructions[str(ip[0])])
        if ip[1][0] == 3:
            text_of += "{0} is offline\n".format(constructions[str(ip[0])])
    text += text_pre_on + text_pre_of + text_of
    bot.sendMessage(update.message.chat_id, text=text)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text="Not a command")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    with open('data.pickle', 'wb') as f:
        pickle.dump(constructions, f)

    # Create the EventHandler and pass it your bot's token.
    updater = Updater("158279031:AAH4d7IwuWy5H8LNxIWY0dEK2eDs1UkcfQ0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start_user", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("status", status)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    # dp.addErrorHandler(error)

    Diagnostic.start()

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
