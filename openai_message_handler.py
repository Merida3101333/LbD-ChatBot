import os
from dotenv import load_dotenv
import openai


# 載入 .env 文件中的環境變數
load_dotenv()
# 從環境變數獲取 OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客戶端
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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
        await update.message.reply_text("抱歉,處理您的訊息時出現了錯誤。")
