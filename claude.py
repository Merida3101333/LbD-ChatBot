import os
import schedule
import time
import telebot
import openai
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 載入 .env 文件中的環境變數
load_dotenv()

# 從環境變數獲取 Telegram Bot Token 和 OpenAI API Key
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_ID = '1924319284'

# 初始化 OpenAI 客戶端
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 初始化 Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """發送歡迎訊息"""
    await update.message.reply_text('歡迎使用 OpenAI 聊天機器人!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理用戶訊息並使用 OpenAI 生成回覆"""
    user_message = update.message.text
    
    try:
        # 使用 OpenAI API 生成回覆
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
    
        bot_reply = response.choices[0].message.content.strip()
        
        # 發送回覆給用戶
        await update.message.reply_text(bot_reply)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        await update.message.reply_text("抱歉，處理您的訊息時出現了錯誤。")

def generate_toeic_questions():
    prompt = "Generate 3 TOEIC reading comprehension questions with answers. Format each question with its options and the correct answer."
    response = client.chat.completions.create(
        model="gpt-4",  # 修正：從 "gpt-4o" 改為 "gpt-4"
        messages=[
            {"role": "system", "content": "You are a TOEIC test creator."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def send_questions():
    questions = generate_toeic_questions()
    bot.send_message(USER_ID, f"Here are your TOEIC questions for {datetime.now().strftime('%Y-%m-%d %H:%M')}:\n\n{questions}")

def schedule_jobs():
    schedule.every().day.at("06:00").do(send_questions)
    schedule.every().day.at("12:00").do(send_questions)
    schedule.every().day.at("18:00").do(send_questions)
    schedule.every().day.at("22:36").do(send_questions)

def main():
    # 創建應用程序並傳入機器人的 token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 添加處理程序
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 設置定時任務
    schedule_jobs()

    # 在單獨的線程中運行 schedule
    import threading
    threading.Thread(target=run_schedule, daemon=True).start()

    # 啟動機器人
    application.run_polling()

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()