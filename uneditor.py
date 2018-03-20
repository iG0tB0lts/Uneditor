from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pickle, sqlite3

msg_dict = {}
chat_list = []


with open('chatinfo.pickle', 'rb') as handle:
    chat_list = pickle.load(handle)


def read_db(msg_id, tn):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("SELECT txt FROM {} WHERE id = {}".format(tn, msg_id))
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data[0]


def see_edit(bot, update):
    msg_id = int(update.edited_message.message_id)
    chat_title = str(update.edited_message.chat.title)
    update.edited_message.reply_text("Message edited! Original message was:\n'{}'".format(read_db(msg_id, chat_title)))



def add_todb(tn, msg_id, msg_txt):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS {} (id INTEGER, txt TEXT)".format(tn))
    c.execute("INSERT INTO {} VALUES ({}, '{}')".format(tn, msg_id, msg_txt))
    conn.commit()
    conn.close()


# Save Message
def save_msg(bot, update):
    chat_title = str(update.message.chat.title)
    chat_id = update.message.chat_id
    msg_id = int(update.message.message_id)
    msg_txt = update.message.text
    msg_dict[msg_id] = msg_txt
    add_todb(chat_title, msg_id, msg_txt)
    # Save chat info
    if chat_id not in chat_list:
        chat_list.append(chat_id)
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
