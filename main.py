from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, BaseFilter
from utils import gen_out_path
from activity_logger import *
import logging


# TODO: manage to recover messages after being offline
# TODO: change the token and take it from a local file
TOKEN = "559626786:AAGKYE0MArTga7alcjpCltov9hjsHQuec9Y"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                    filename=r"C:\Projects\festivalBot\err.log")


# TODO: manage to write fucking unicode FML i hate encodings
logger = logging.getLogger(__name__)
groups = load_groups(JSON_PATH)


def log_point(update):
    try:
        if int(update.message.text) not in MISSION_SCORE:
            return False
        # TODO: add the points to the relevant group
    except ValueError:
        #TODO: this
        logger.error('Could not log point, from user %s message %s')
        return False


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update.message.text, error)

class CostumFilter(BaseFilter):
    def filter(self, message):
        return message.text.startswith("#") or message.photo

my_filter = CostumFilter()

def start(bot, update):
    """

    display the start message
    """
    # TODO: add a normal start message with hebrew!
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def save_photo(bot, update):
    # TODO: use message.from_user.is_bot and ignore all bot messages
    # TODO: do the same for a video
    if update.message.photo:
        # TODO: i noticed that when one photo is sent, i am recieving a list of images, need to get the largest one with a file size limit
        photo_file = update.message.photo[-1].get_file()
        # TODO: before downloading, check available space in case of spammers, send me a notification if there is a problem
        photo_file.download(gen_out_path(group_id=str(update.message.chat.id)))
    bot.send_message(chat_id=update.message.chat_id, text="photo!")


def save_vid(bot, update):
    if update.message.video:
        if update.message.video:
            video = bot.get_file(update.message.video.file_id)
            video.download(gen_out_path("mpeg4", group_id=str(update.message.chat.id)))
    bot.send_message(chat_id=update.message.chat_id, text="video!")


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(CommandHandler('join', add_user_to_group))
    # dispatcher.add_handler(CommandHandler('score', get_score))
    dispatcher.add_handler(MessageHandler(Filters.photo, save_photo))
    dispatcher.add_handler(MessageHandler(Filters.video, save_vid))
    dispatcher.add_error_handler(error)
    updater.start_polling()
    # TODO: log the results to a file every x secs
    print("Running")
    updater.idle()


if __name__ == '__main__':
    main()
