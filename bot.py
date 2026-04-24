import telebot
import requests
import time
import hashlib

# --- إعدادات التوكن والمفاتيح ---
BOT_TOKEN = '8503828764:AAEZScCTpA3I5Dwpg8rliweyeGFZo-HIPJM'
APP_KEY = '532804'
APP_SECRET = 'WSGl2s7FrNhXVxsmTpgMEthlHeIOKzeX'
TRACKING_ID = 'Med-Jamel23' في لوحة تحكم Portals

bot = telebot.TeleBot(BOT_TOKEN)

def generate_affiliate_link(product_url):
    """دالة للتواصل مع API علي إكسبريس وتحويل الرابط"""
    endpoint = "https://api-sg.aliexpress.com/sync" # السيرفر الآسيوي
    
    # المعايير المطلوبة للـ API
    params = {
        'method': 'aliexpress.affiliate.link.generate',
        'app_key': APP_KEY,
        'sign_method': 'md5',
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        'format': 'json',
        'v': '2.0',
        'promotion_link_type': '0',
        'source_values': product_url,
        'tracking_id': TRACKING_ID
    }

    # عملية التوقيع (Signing) - ضرورية لأمان الطلب
    query = "".join(f"{k}{v}" for k, v in sorted(params.items()))
    sign_str = f"{APP_SECRET}{query}{APP_SECRET}"
    params['sign'] = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        # استخراج الرابط المطور من النتيجة
        aff_link = data['aliexpress_affiliate_link_generate_response']['resp_result']['result']['promotion_links']['promotion_link'][0]['promotion_link']
        return aff_link
    except Exception as e:
        print(f"Error: {e}")
        return None

# --- التعامل مع الرسائل في تليجرام ---

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "مرحباًBestDealsProoo! أرسل لي أي رابط من AliExpress وسأقوم بتحويله لرابط عمولة فوراً.")

@bot.message_handler(func=lambda message: "aliexpress.com" in message.text)
def handle_link(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "جاري تحويل الرابط... ⏳")
    
    aff_link = generate_affiliate_link(url)
    
    if aff_link:
        text = f"✅ **تم إنشاء رابط العمولة بنجاح:**\n\n{aff_link}"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "عذراً، حدث خطأ أثناء تحويل الرابط. تأكد من صحة المفاتيح.")

print("البوت يعمل الآن...")
bot.infinity_polling()
