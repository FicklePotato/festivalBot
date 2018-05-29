#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, BaseFilter
from utils import gen_out_path, enter_dump_cycle
from activity_logger import *
from myToken import *
import logging


# TODO: manage to recover messages after being offline
# TODO: change the token and take it from a local file

ADMIN_IDS = [409589602, 596310448]
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                    filename=r"err.log")


# TODO: manage to write fucking unicode FML i hate encodings
logger = logging.getLogger(__name__)
groups = load_groups(JSON_PATH)


def log_point(bot, update):
    try:
        mission = update.message.caption
        if mission not in MISSION_SCORE:
            return False
        if update.message.chat.id not in groups:
            groups[update.message.chat.id] = Group(update.message.chat.id, [], update.message.chat.title)
        if mission in groups[update.message.chat.id].completed_missions:
            bot.send_message(chat_id=update.message.chat.id, text="המשימה {0} כבר הושלמה.".format(mission))
            return False
        else:
            groups[update.message.chat.id].complete_mission(mission)
            bot.send_message(chat_id=update.message.chat.id, text="קיבלתם {0} נקודות!".format(MISSION_SCORE[mission]))
            return mission
    except (ValueError, TypeError) as e:
        logger.info('Could not log point, from user %s message %s', e)
        return False


def error(bot, update, error):
    """Log Errors caused by Updates."""
    try:
        if update is None:
            logger.error("Got error %s", error)
        else:
            logger.warning('Update "%s" caused error "%s"', update.message.text, error)
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass


class CostumFilter(BaseFilter):
    def filter(self, message):
        # TODO filter out bots
        return message.chat.type == "group"


class AdminFilter(BaseFilter):
    def filter(self, message):
        # TODO filter out bots
        return message.chat.id in ADMIN_IDS

my_filter = CostumFilter()
admin_filter = AdminFilter()


def start(bot, update):
    """

    display the start message
    """
    # TODO: add a normal start message with hebrew!
    if my_filter.filter(update.message):
        bot.send_message(chat_id=update.message.chat.id, text="I'm a bot, please talk to me!")


def help(bot, update):
    if my_filter.filter(update.message):
        bot.send_message(chat_id=update.message.chat.id, text="/score - show your group's score.")


def save_photo(bot, update):
    if update.message.photo:
        mission = log_point(bot, update)
        if mission:
            photo_file = update.message.photo[-1].get_file()
            photo_file.download(gen_out_path(group_id=str(update.message.chat.id), prefix=mission))


def save_vid(bot, update):
    if update.message.video:
        mission = log_point(bot, update)
        if mission:
            video = bot.get_file(update.message.video.file_id)
            video.download(gen_out_path("mpeg4", group_id=str(update.message.chat.id), prefix=mission))


def get_score(bot, update):
    if update.message.chat.id in groups:
        bot.send_message(chat_id=update.message.chat.id, text="יש לכם {0} נקודות :)".format(groups[update.message.chat.id].get_score()))
    else:
        # TODO: send something
        pass


def get_allscore(bot, update):
    if admin_filter.filter(update.message):
        msg = '\r\n'.join([' - '.join((g.title, str(g.get_score()))) for g in groups.values()])
        if msg:
            bot.send_message(chat_id=update.message.chat.id, text=msg)


def sendto(bot, update):
    if admin_filter.filter(update.message):
        try:
            _, group_title, msg = update.message.text.split("###")
            if group_title == "AlL":
                for group in groups.values():
                    # TODO: make sure the bot is sending a msg only to groups it is part of.
                    bot.send_message(chat_id=group.id, text=msg)
                return
            group = [g for g in groups.values() if group_title == g.title]
            if group:
                group = group[0]
                bot.send_message(chat_id=group.id, text=msg)
            else:
                bot.send_message(chat_id=update.message.chat.id, text="Group  not found.")
        except ValueError:
            bot.send_message(chat_id=update.message.chat.id, text="Bad command. got ValueError.")

def main():
    try:
        updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('score', get_score))
        dispatcher.add_handler(CommandHandler('allscore', get_allscore))
        dispatcher.add_handler(CommandHandler('sendto', sendto))
        dispatcher.add_handler(MessageHandler(Filters.photo & my_filter, save_photo))
        dispatcher.add_handler(MessageHandler(Filters.video & my_filter, save_vid))
        dispatcher.add_error_handler(error)
        updater.start_polling()
        print("Running")
        enter_dump_cycle(groups)
        updater.idle()
    finally:
        dump_groups(JSON_PATH, groups)


if __name__ == '__main__':
    main()
