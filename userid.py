import telebot

# 替換為你的 bot token
TOKEN = '6587009607:AAFnt8yPinyOMuY_OeiV4P7lcxJuf_2wVYw'

# 初始化 bot
bot = telebot.TeleBot(TOKEN)

# 替換為你想發送消息的用戶 ID
USER_ID = '1924319284'

def send_message_to_user():
    try:
        message = "Hello! 家誠你還好嗎？。"
        bot.send_message(USER_ID, message)
        print(f"消息已成功發送給用戶 {USER_ID}")
    except Exception as e:
        print(f"發送消息時出錯: {e}")

if __name__ == "__main__":
    send_message_to_user()