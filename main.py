# -*- coding: utf-8 -*-
# بوت تيليجرام: بث مباشر + اشتراك إجباري + احصائيات


import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

TOKEN = "8263029264:AAF9OjHICRjeWdVMldhxdfMEzDaafsgt5w8"
CHANNEL_USERNAME = "@egylleague"
LIVE_URL = "https://www.youtube.com/embed/QdmMCkF4Z4A"
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)

# دالة تسجيل المستخدمين
def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, 'w').close()
    with open(USERS_FILE, 'r+') as f:
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(str(user_id) + "\n")

# دالة التحقق من الاشتراك
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    save_user(user_id)
    if is_subscribed(user_id):
        send_live_button(user_id)
    else:
        send_subscribe_request(user_id)

def send_subscribe_request(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
        InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")
    )

    text = (
        "🚨 للوصول إلى البث المباشر، يجب أولاً الاشتراك في قناتنا الرسمية.\n\n"
        "بعد الاشتراك، اضغط على الزر 👇 'تحقق من الاشتراك'."
    )
    bot.send_message(user_id, text, reply_markup=markup)

def send_live_button(user_id):
    markup = InlineKeyboardMarkup()
    webapp = WebAppInfo(LIVE_URL)
    markup.add(InlineKeyboardButton("🎥 فتح البث المباشر الآن", web_app=webapp))

    bot.send_message(
        user_id,
        "🎬 أهلاً بك في بث Flex Aflam المباشر!\n\nاضغط الزر بالأسفل لفتح البث داخل تيليجرام 🔥",
        reply_markup=markup
    )

# ✅ دالة تحقق الاشتراك بعد التعديل لتجاهل أخطاء انتهاء الوقت
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.message.chat.id
    try:
        if is_subscribed(user_id):
            try:
                bot.answer_callback_query(call.id, "✅ تم التحقق! أنت مشترك ✅")
            except:
                pass
            send_live_button(user_id)
        else:
            try:
                bot.answer_callback_query(call.id, "❌ لسه مش مشترك، اشترك في القناة أولًا.")
            except:
                pass
    except Exception as e:
        print(f"⚠️ خطأ أثناء التحقق من الاشتراك: {e}")

# 🧮 أمر الإحصائيات
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        ADMIN_ID = 123456789  # ← بدّلها بـ ID حسابك
        if user_id != ADMIN_ID:
            bot.send_message(user_id, "🚫 هذا الأمر مخصص للإدارة فقط.")
            return

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = f.read().splitlines()
            total_users = len(users)
    else:
        total_users = 0

    bot.send_message(
        message.chat.id,
        f"📊 إحصائيات البوت:\n\n👥 عدد المستخدمين المسجلين: {total_users}"
    )

print("✅ البوت شغال... جرب /start و /stats")
bot.polling(none_stop=True)
