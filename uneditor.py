from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pickle

msg_dict = {}

with open('message.pickle', 'rb') as handle:
    msg_dict = pickle.load(handle)


def see_edit(bot, update):
    global msg_dict
    edit_id = update.edited_message.message_id
    update.edited_message.reply_text("Message edited! Original message was:'{}'".format(msg_dict["{}".format(edit_id)]))


# Save Message
def save_msg(bot, update):
    global msg_dict
    msg_txt = update.message.text
    msg_id = update.message.message_id
    msg_dict["{}".format(msg_id)] = msg_txt
    with open('message.pickle', 'wb') as handle:  # Save messages
        pickle.dump(msg_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# ################      MAIN        ##################
def main():
    updater = Updater(token='')
    dp = updater.dispatcher

    # Dispatcher for commands

    # Dispatcher for msgs
    dp.add_handler(MessageHandler(Filters.text, save_msg))
    dp.add_handler(MessageHandler(Filters.text, see_edit, edited_updates=True))
    # Begin polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
