import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client, handle_file

# Coqui का फ्री ऑफिशियल क्लाउड स्पेस जो बिना किसी खर्चे के AI आवाज़ जनरेट करेगा
print("Connecting to Free Voice AI...")
client = Client("coqui/xtts")

# आपकी आवाज़ की फाइल का नाम जो आप GitHub पर अपलोड करोगे
VOICE_SAMPLE = "my_voice.wav"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! बोट तैयार है। मुझे कोई भी टेक्स्ट भेजें, मैं उसे आपकी आवाज़ में बदल कर भेजूँगा।")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("आवाज़ जनरेट हो रही है, कृपया थोड़ा इंतज़ार करें...")

    try:
        # क्लाउड पर टेक्स्ट और आपकी आवाज़ भेजकर क्लोन ऑडियो जनरेट करना
        result = client.predict(
            prompt=user_text,
            language="hi",
            audio_file_pth=handle_file(VOICE_SAMPLE),
            agree=True,
            api_name="/predict"
        )
        
        # जनरेट हुई ऑडियो फाइल का पाथ (result[0])
        audio_path = result[0]

        # टेलीग्राम पर वॉइस नोट के रूप में भेजना
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_voice(voice=audio_file)
            
    except Exception as e:
        await update.message.reply_text(f"एरर आ गया: {str(e)}")

if __name__ == '__main__':
    # यहाँ अपना टेलीग्राम बोट टोकन डालें (जो BotFather से मिला था)
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot is running...")
    app.run_polling()
  
