from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pickle, sqlite3

chat_list = []


def read_list():
    with open('chatinfo.pickle', 'rb') as handle:
        cl = pickle.load(handle)
    return cl


def read_db(msg_id):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("SELECT txt FROM messages WHERE id = {}".format(msg_id))
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data[0]


def see_edit(bot, update):
    msg_id = int(update.edited_message.message_id)
    update.edited_message.reply_text("Message edited! Original message was:\n'{}'".format(read_db(msg_id)))


def add_todb(msg_id, msg_txt):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER, txt TEXT)")
    c.execute("INSERT INTO messages VALUES ({}, '{}')".format(msg_id, msg_txt))
    conn.commit()
    conn.close()


def save_msg(bot, update):
    chat_id = str(update.message.chat_id)
    msg_id = int(update.message.message_id)
    msg_txt = update.message.text
    add_todb(msg_id, msg_txt)
    # Save chats in which bot exists
    if chat_id not in chat_list:
        chat_list.append(chat_id)
        with open('chatinfo.pickle', 'wb') as handle:
            pickle.dump(chat_list, handle)


def maintain(bot, update):
    chat_list = read_list()
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
