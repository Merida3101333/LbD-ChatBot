import os
import schedule
from dotenv import load_dotenv
import time
import telebot
import openai
from datetime import datetime

# 載入 .env 文件中的環境變數
load_dotenv()

# 從環境變數獲取 Telegram Bot Token 和 OpenAI API Key
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_ID = '1924319284'

# 初始化Telegram bot和OpenAI
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_toeic_questions():
    prompt = "Generate 3 TOEIC reading comprehension questions with answers. Format each question with its options and the correct answer."
    response = client.chat.completions.create(
        model="gpt-4o",
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

if __name__ == "__main__":
    schedule_jobs()
    while True:
        schedule.run_pending()
        time.sleep(1)