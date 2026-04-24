import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import requests

# 1. إعدادات الوصول (التوكن الخاص بك)
API_TOKEN = '8503828764:AAEZScCTpA3I5Dwpg8rliweyeGFZo-HIPJM'
bot = telebot.TeleBot(API_TOKEN)

# 2. بيانات الأفلييت (تأكد أن هذه الأرقام مطابقة لحسابك في Portals)
app_key = '532804'
secret_key = 'WSGl2s7FrNhXVxsmTpgMEthlHeIOKzeX'
tracking_id = 'Med-Jamel23'

aliexpress = AliexpressApi(app_key, secret_key, models.Language.EN, models.Currency.EUR, tracking_id)

def get_final_url(url):
    """دالة لفك الروابط المختصرة والحصول على الرابط الأصلي للمنتج"""
    try:
        session = requests.Session()
        resp = session.head(url, allow_redirects=True, timeout=10)
        return resp.url
    except:
        return url

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("⭐️ قناة العروض ⭐️", url="https://t.me/AliXPromotion")
    markup.add(btn)
    bot.reply_to(message, "أهلاً بك أبو زيد في بوت تحويل روابط AliExpress! 🛒\n\nأرسل لي رابط المنتج وسأقوم بتجهيزه لك فوراً.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def process_links(message):
    # استخراج الرابط من نص الرسالة
    match = re.search(r'(https?://\S+)', message.text)
    if not match:
        bot.reply_to(message, "من فضلك أرسل رابطاً صحيحاً.")
        return

    original_url = match.group(1)
    
    if "aliexpress.com" in original_url:
        msg = bot.send_message(message.chat.id, "جاري تحويل الرابط... ⏳")
        try:
            # خطوة مهمة: الحصول على الرابط الحقيقي للمنتج
            real_url = get_final_url(original_url)
            
            # تحويله لرابط أفلييت خاص بك
            aff_links = aliexpress.get_affiliate_links(real_url)
            
            if aff_links:
                final_aff_url = aff_links[0].promotion_link
                # إرسال النتيجة النهائية
                bot.edit_message_text(f"✅ تم تجهيز الرابط الخاص بك:\n\n🔗 {final_aff_url}\n\nتمنياتنا لك بالتوفيق في مبيعاتك! 🚀", 
                                      message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ لم أتمكن من تحويل هذا الرابط. تأكد أنه رابط منتج متاح للأفلييت.", message.chat.id, msg.message_id)
        
        except Exception as e:
            bot.edit_message_text(f"⚠️ حدث خطأ فني. تأكد من تفعيل الـ API في Portals.", message.chat.id, msg.message_id)
    else:
        bot.send_message(message.chat.id, "عذراً، أقبل روابط AliExpress فقط.")

bot.infinity_polling()
