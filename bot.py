import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re

# التوكن الخاص بك تم وضعه هنا
API_TOKEN = '8503828764:AAEZScCTpA3I5Dwpg8rliweyeGFZo-HIPJM'
bot = telebot.TeleBot(API_TOKEN)

# إعدادات علي إكسبريس (تأكد من صحتها)
aliexpress = AliexpressApi('532804', 'qW3MlLGKtt7jnZOg8KkHpfCbTaac2LOq',
                           models.Language.EN, models.Currency.EUR, 'default')

# تعريف الكيبورد (زر واحد بسيط للتجربة)
keyboardStart = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton("⭐️ أحدث العروض ⭐️", url="https://t.me/AliXPromotion")
keyboardStart.add(btn1)

@bot.message_handler(commands=['start'])
def welcome_user(message):
    bot.send_message(
        message.chat.id,
        "مرحباً بك! أرسل رابط المنتج وسأقوم بتحويله لك.",
        reply_markup=keyboardStart)

@bot.message_handler(func=lambda message: True)
def handle_links(message):
    if "aliexpress.com" in message.text:
        wait_msg = bot.send_message(message.chat.id, "جاري تجهيز الرابط... ⏳")
        try:
            # استخراج الرابط من النص
            link = re.findall(r'https?://\S+', message.text)[0]
            # تحويل الرابط عبر الأفلييت
            res = aliexpress.get_affiliate_links(link)
            aff_link = res[0].promotion_link
            bot.edit_message_text(f"✅ تفضل الرابط الخاص بك:\n{aff_link}", message.chat.id, wait_msg.message_id)
        except Exception as e:
            bot.edit_message_text("حدث خطأ أثناء تحويل الرابط. تأكد من صحة الرابط.", message.chat.id, wait_msg.message_id)
    else:
        bot.send_message(message.chat.id, "من فضلك أرسل رابط AliExpress صحيح.")

# تشغيل البوت
bot.infinity_polling()
