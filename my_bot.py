import telebot
my_bot = telebot.TeleBot('5845821079:AAHRi3fimC5IDuEpnecRzfhluSrcHVvLJlY')


@my_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        my_bot.send_message(message.from_user.id, "Привет, я очень рад пообщаться,"
                                                  "чем я могу тебе помочь?")
    elif message.text == "/help":
        my_bot.send_message(message.from_user.id, "Напиши привет")
    else:
        my_bot.send_message(message.from_user.id, "Напиши /help.")


my_bot.polling(none_stop=True, interval=0)
