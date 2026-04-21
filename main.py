import telebot
from telebot import types
import google.generativeai as genai
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = '6727896662:AAElrKm8QvwKJl-yfjzQ-BYHPFmO-jxDRLk'
GEMINI_API_KEY = 'AIzaSyBGoeHZIbyJuWo1bLNcO7-A_EOK52Vg61A'
CHANNEL_LINK = 'https://t.me/kohli_k_007' 
OWNER_ID = '@SEE_MY_DICK_ALWAYS' 
PHOTO_URL = 'https://telegra.ph/file/0c3f59e66cb7111ed6263.jpg' 

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
    btn2 = types.InlineKeyboardButton("👤 Owner", callback_data="owner_info")
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    user_name = message.from_user.first_name
    welcome_msg = f"Namaste {user_name}! 🙏\n\nMain ek smart AI bot hoon. Sawal puchiye!"
    try:
        bot.send_photo(message.chat.id, PHOTO_URL, caption=welcome_msg, reply_markup=main_menu())
    except:
        bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "owner_info":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"👑 **Owner ID:** {OWNER_ID}")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        prompt = f"Answer this in Hindi or Hinglish as a friendly assistant: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "AI thoda busy hai.")

if __name__ == "__main__":
    keep_alive()
    print("Bot is running...")
    bot.infinity_polling()
    
