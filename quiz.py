import os
from dotenv import load_dotenv
import sqlite3
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
import asyncio

# 載入環境變量
load_dotenv()

# 設置 Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 連接到 SQLite 數據庫
conn = sqlite3.connect('quiz_bot.db')
cursor = conn.cursor()

# 創建題目表和用戶表
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_answer TEXT,
    explanation TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS subscribers (
    user_id INTEGER PRIMARY KEY
)
''')

conn.commit()

async def start(update, context):
    user_id = update.effective_user.id
    cursor.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await update.message.reply_text("您已成功訂閱每日測驗！")

async def send_quiz():
    # 從數據庫中隨機選擇三道題目
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 3")
    questions = cursor.fetchall()

    # 獲取所有訂閱者
    cursor.execute("SELECT user_id FROM subscribers")
    subscribers = cursor.fetchall()

    for user_id in subscribers:
        quiz_message = "今日測驗題目：\n\n"
        for i, q in enumerate(questions, 1):
            quiz_message += f"{i}. {q[1]}\n"
            quiz_message += f"A. {q[2]}\nB. {q[3]}\nC. {q[4]}\nD. {q[5]}\n"
            quiz_message += f"正確答案：{q[6]}\n"
            quiz_message += f"解釋：{q[7]}\n\n"

        # 發送消息給每個訂閱者
        await context.bot.send_message(chat_id=user_id[0], text=quiz_message)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 添加處理程序
    application.add_handler(CommandHandler("start", start))

    # 設置定時任務
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_quiz, 'cron', hour='6,12,18')
    scheduler.start()

    # 啟動機器人
    application.run_polling()

if __name__ == '__main__':
    main()