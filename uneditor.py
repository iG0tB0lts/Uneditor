from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pickle

msg_dict = {}
chat_list = []

with open('message.pickle', 'rb') as handle:
    msg_dict = pickle.load(handle)

with open('chatinfo.pickle', 'rb') as handle:
    chat_list = pickle.load(handle)


def see_edit(bot, update):
    edit_id = update.edited_message.message_id
    update.edited_message.reply_text("Message edited! Original message was:\n'{}'".format(msg_dict["{}".format(edit_id)]))


def write_to_file():
    with open('message.pickle', 'wb') as handle:  # Save messages
        pickle.dump(msg_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# Save Message
def save_msg(bot, update):
    chat_id = str(update.message.chat_id)
    msg_id = update.message.message_id
    msg_dict["{}".format(msg_id)] = update.message.text
    write_to_file()
    # Save chat info
    if chat_id not in chat_list:
        chat_list.append("{}".format(chat_id))
        with open('chatinfo.pickle', 'wb') as handle:
            pickle.dump(chat_list, handle)


def maintain(bot, update):
    for i in chat_list:
        bot.sendMessage(chat_id=i, text='Bot is down for maintenance.')


# ################      MAIN        ##################
def main():
    updater = Updater(token='')
    dp = updater.dispatcher

    # Dispatcher for commands
    dp.add_handler(CommandHandler("maint", maintain, filters=Filters.user()))

    # Dispatcher for msgs
    dp.add_handler(MessageHandler(Filters.text, save_msg))
    dp.add_handler(MessageHandler(Filters.text, see_edit, edited_updates=True))
    # Begin polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
