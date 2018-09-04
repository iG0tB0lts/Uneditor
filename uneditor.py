from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pickle, sqlite3


def read_db(tn, msg_id):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("SELECT txt FROM '{}' WHERE id = {}".format(tn, msg_id))
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data[0]


def del_old(tn):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("DELETE FROM '{}' WHERE date <= date('now', '-2 day')".format(tn))
    conn.commit()
    conn.close()

def see_edit(bot, update):
    chat_id = str(update.edited_message.chat_id)
    msg_id = int(update.edited_message.message_id)
    update.edited_message.reply_text("Message edited! Original message was:\n'{}'".format(read_db(chat_id, msg_id)))
    del_old(chat_id)


def add_todb(tn, msg_id, msg_txt):
    conn = sqlite3.connect('msgs.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS '{}' (id INTEGER, txt TEXT, date INTEGER)".format(tn))
    c.execute("INSERT INTO '{}' VALUES (?, ?, date('now'))".format(tn), (msg_id, msg_txt))
    conn.commit()
    conn.close()


def save_msg(bot, update):
    chat_id = str(update.message.chat_id)
    msg_id = int(update.message.message_id)
    msg_txt = update.message.text
    ckey = ['Connect Four\n\n', 'Tic-Tac-Toe\n\n', 'Rock-Paper-Scissors\n\n', 'Russian Roulette\n\n', 'Checkers\n\n', 'Pool Checkers\n\n']
    if all(word not in str(msg_txt) for word in ckey):
        add_todb(chat_id, msg_id, msg_txt)


def init(bot, update):
    update.message.reply_text("Hi! Simply send a message, then edit it.\nAdd to groups for additional benefit!")
    


# ################      MAIN        ##################
def main():
    updater = Updater(token='')
    dp = updater.dispatcher

    # Dispatcher for commands
    dp.add_handler(CommandHandler("start", init))

    # Dispatcher for msgs
    dp.add_handler(MessageHandler(Filters.text, save_msg))
    dp.add_handler(MessageHandler(Filters.text, see_edit, edited_updates=True))
    # Begin polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
