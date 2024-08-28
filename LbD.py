import telebot

# 替換為你的bot token
TOKEN = '6587009607:AAFnt8yPinyOMuY_OeiV4P7lcxJuf_2wVYw'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['8787lin', 'help'])
def send_welcome(message):
    bot.reply_to(message, "你好！謝謝尼。")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()