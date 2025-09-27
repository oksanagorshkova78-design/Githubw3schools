import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator
from gtts import gTTS

# 🔑 Токен бота
TELEGRAM_TOKEN = "8057524130:AAFTHa3_CXEH3ZGZ9J5mmJHVLidcts8g88Q"
# 🌍 Язык для перевода (ISO код)
TARGET_LANG = "en"

# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🖐\nОтправь мне любой текст, и я переведу его на английский с озвучкой 🎧"
    )

# 🔄 Перевод текста и озвучка
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_text = update.message.text

    try:
        # Перевод Stable API
        translated_text = GoogleTranslator(source='auto', target=TARGET_LANG).translate(original_text)

        # Отправим перевод
        await update.message.reply_text(f"Перевод ({TARGET_LANG}):\n{translated_text}")

        # Озвучка
        tts = gTTS(translated_text, lang=TARGET_LANG)
        audio_file = "audio.mp3"
        tts.save(audio_file)

        # Отправка аудио
        await update.message.reply_voice(open(audio_file, 'rb'))

        # Удаляем файл после отправки
        os.remove(audio_file)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# 🔧 Запуск приложения
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен 🚀")
    app.run_polling()