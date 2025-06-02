import os
import openai
import replicate
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка токенов
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот. Напиши мне вопрос или /image <запрос> для генерации картинки.")

# Чат с GPT
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка GPT: {str(e)}")


# Генерация изображения
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("❗️Напиши запрос после команды, пример:\n/image замок в горах на закате")
        return

    try:
        client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        output = client.run(
            "stability-ai/stable-diffusion:db21e45b23b0a601b9ee1c83e77c1cc2826f69eb82451c3b26cb05d7df0b3dfb",
            input={"prompt": prompt}
        )
        await update.message.reply_photo(photo=output[0], caption="🎨 Сгенерировано")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка генерации изображения: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Бот запущен...")
    app.run_polling()
