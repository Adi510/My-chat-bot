import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- SERVER FOR RENDER (Bot ko 24/7 zinda rakhne ke liye) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running perfectly!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
TOKEN = '6727896662:AAElrKm8QvwKJl-yfjzQ-BYHPFmO-jxDRLk'
GEMINI_KEY = 'AIzaSyAQ5Ci3QQCmlZ4a0C6etKsIu_3IVLNygXI' # Aapki nayi key add kar di hai

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "Namaste! 🙏\n\n"
        "Main ek Smart AI Bot hoon. Ab main is group (ya chat) mein "
        "har ek message ka reply dunga. Kuch bhi puchiye!"
    )
    bot.reply_to(message, welcome_text)

# --- AI REPLY LOGIC (Sab kuch ka jawab dene ke liye) ---
@bot.message_handler(func=lambda message: True)
def reply_all(message):
    # Agar message kisi bot ne bheja hai toh reply mat karna (loop se bachne ke liye)
    if message.from_user.is_bot:
        return

    try:
        # User ke message ko Gemini AI ke paas bhejna
        # Humne AI ko instruction diya hai ki short aur friendly reply de
        chat_prompt = f"Answer this in Hindi or Hinglish shortly: {message.text}"
        response = model.generate_content(chat_prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
    except Exception as e:
        # Agar koi error aaye toh chup rehna ya simple reply dena
        print(f"Error: {e}")
        # bot.reply_to(message, "Hmm... main samajh nahi pa raha hoon.")

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling()
