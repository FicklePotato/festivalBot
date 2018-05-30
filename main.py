#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, BaseFilter
from activity_logger import *
from utils import enter_dump_cycle, gen_out_path
from myToken import *
from consts import *
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                    filename=r"err.log")


# TODO: manage to write fucking unicode FML i hate encodings
logger = logging.getLogger(__name__)
groups = load_groups(JSON_PATH)


def log_point(bot, update):
    try:
        mission = update.message.caption
        if update.message.chat.id not in groups:
            groups[update.message.chat.id] = Group(update.message.chat.id, [], update.message.chat.title)
        if mission not in MISSION_SCORE:
            if mission is None:
                bot.send_message(chat_id=update.message.chat.id, text="משימות בלי תיאור לא נחשבות :( שלחו את התמונה שוב עם מספר המשימה שהושלמה.".format(mission))
            else:
                bot.send_message(chat_id=update.message.chat.id, text="המשימה {0} לא קיימת.".format(mission))
            return False
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


def first_message(bot, update):
    if update.message.chat.id not in groups:
        groups[update.message.chat.id] = Group(update.message.chat.id, [], update.message.chat.title)
        bot.send_message(chat_id=update.message.chat.id, text=START_MSG)


def help(bot, update):
    if my_filter.filter(update.message):
        bot.send_message(chat_id=update.message.chat.id, text=HELP_MSG)


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
        group = groups[update.message.chat.id]
        bot.send_message(chat_id=update.message.chat.id, text="יש לכם {0} נקודות :)\r\n"
                                                              "המשימות שהושלמו הן: {1}".format(group.get_score(),
                                                            ', '.join(str(i) for i in group.completed_missions)))

    else:
        groups[update.message.chat.id] = Group(update.message.chat.id, [], update.message.chat.title)
        bot.send_message(chat_id=update.message.chat.id,
                         text="עוד לא קיבלתם נקודות :(".format(groups[update.message.chat.id].get_score()))


def get_allscore(bot, update):
    if admin_filter.filter(update.message):
        msg = '\r\n'.join([' - '.join((g.title, g.id, str(g.get_score()))) for g in groups.values()])
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
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('score', get_score))
        dispatcher.add_handler(CommandHandler('allscore', get_allscore))
        dispatcher.add_handler(CommandHandler('sendto', sendto))
        dispatcher.add_handler(MessageHandler(Filters.photo & my_filter, save_photo))
        dispatcher.add_handler(MessageHandler(Filters.video & my_filter, save_vid))
        dispatcher.add_handler(MessageHandler(Filters.text, first_message))
        dispatcher.add_error_handler(error)
        updater.start_polling()
        print("Running")
        enter_dump_cycle(groups)
        updater.idle()
    finally:
        dump_groups(JSON_PATH, groups)


if __name__ == '__main__':
    main()
