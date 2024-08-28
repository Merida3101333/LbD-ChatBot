import telebot
import threading
import time

# 替換為你的bot token
TOKEN = '6587009607:AAFnt8yPinyOMuY_OeiV4P7lcxJuf_2wVYw'

bot = telebot.TeleBot(TOKEN)

# 全局變量，用於存儲訂閱用戶的 chat_id
subscribed_users = set()

@bot.message_handler(commands=['8787lin', 'help'])
def send_welcome(message):
    bot.reply_to(message, "你好！謝謝尼。使用 /subscribe 來接收定時數字。")

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    chat_id = message.chat.id
    subscribed_users.add(chat_id)
    bot.reply_to(message, "你已訂閱定時數字服務。每10秒你將收到一個數字。")

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    chat_id = message.chat.id
    if chat_id in subscribed_users:
        subscribed_users.remove(chat_id)
        bot.reply_to(message, "你已取消訂閱定時數字服務。")
    else:
        bot.reply_to(message, "你還沒有訂閱定時數字服務。")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def send_number():
    number = 1
    while True:
        for chat_id in subscribed_users:
            try:
                bot.send_message(chat_id, f"你的數字是：{number}")
            except Exception as e:
                print(f"發送消息給 {chat_id} 時出錯: {e}")
        number += 1
        time.sleep(10)

# 創建並啟動定時發送數字的線程
number_thread = threading.Thread(target=send_number)
number_thread.start()

# 啟動機器人
bot.polling()