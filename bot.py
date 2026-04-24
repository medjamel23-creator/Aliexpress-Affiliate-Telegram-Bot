import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import requests
import json
import urllib.parse
from urllib.parse import urlparse, parse_qs

# إعداد البوت والـ API
bot = telebot.TeleBot('6613740819:AAEiGrOSCcuVNQTrzkhbJ4Bg29oBm6UU6nw')
aliexpress = AliexpressApi('502336', 'qW3MlLGKtt7jnZOg8KkHpfCbTaac2LOq',
                           models.Language.EN, models.Currency.EUR, 'default')

# إعداد الكيبورد الأساسي
keyboardStart = types.InlineKeyboardMarkup(row_width=1)
btn_g = types.InlineKeyboardButton("⭐️ألعاب لجمع العملات المعدنية⭐️", callback_data="games")
btn_c = types.InlineKeyboardButton("⭐️تخفيض العملات على منتجات السلة 🛒⭐️", callback_data='click')
keyboardStart.add(btn_g, btn_c)

# كيبورد الاشتراك والقنوات
keyboard = types.InlineKeyboardMarkup(row_width=1)
btn_sub = types.InlineKeyboardButton("❤️ اشترك في القناة للمزيد من العروض ❤️", url="https://t.me/AliXPromotion")
keyboard.add(btn_sub)

# كيبورد الألعاب
keyboard_games = types.InlineKeyboardMarkup(row_width=1)
games_links = [
    ("⭐️ صفحة مراجعة وجمع النقاط يوميا ⭐️", "https://s.click.aliexpress.com/e/_on0MwkF"),
    ("⭐️ لعبة Merge boss ⭐️", "https://s.click.aliexpress.com/e/_DlCyg5Z"),
    ("⭐️ لعبة Fantastic Farm ⭐️", "https://s.click.aliexpress.com/e/_DBBkt9V"),
    ("⭐️ لعبة قلب الاوراق Flip ⭐️", "https://s.click.aliexpress.com/e/_DdcXZ2r"),
    ("⭐️ لعبة GoGo Match ⭐️", "https://s.click.aliexpress.com/e/_DDs7W5D")
]
for text, url in games_links:
    keyboard_games.add(types.InlineKeyboardButton(text, url=url))

@bot.message_handler(commands=['start'])
def welcome_user(message):
    bot.send_message(
        message.chat.id,
        "مرحبا بك، ارسل لنا رابط المنتج الذي تريد شرائه لنوفر لك افضل سعر له 👌 \n",
        reply_markup=keyboardStart)

@bot.callback_query_handler(func=lambda call: call.data == 'click')
def button_click(callback_query):
    text = "✅1-ادخل الى السلة من هنا:\n" \
           " https://s.click.aliexpress.com/e/_opGCtMf \n" \
           "✅2-قم باختيار المنتجات التي تريد تخفيض سعرها\n" \
           "✅3-اضغط على زر دفع ليحولك لصفحة التأكيد \n" \
           "✅4-اضغط على الايقونة في الاعلى وانسخ الرابط هنا في البوت لتتحصل على رابط التخفيض"
    
    img_link1 = "https://i.postimg.cc/HkMxWS1T/photo-5893070682508606111-y.jpg"
    bot.send_photo(callback_query.message.chat.id, img_link1, caption=text, reply_markup=keyboard)

def get_affiliate_links(message, message_id, link):
    try:
        # جلب الروابط (تم تصحيح جلب الروابط لتجنب الأخطاء)
        res = aliexpress.get_affiliate_links(link)
        affiliate_link = res[0].promotion_link if res else "غير متوفر"
        
        # محاولة جلب تفاصيل المنتج
        try:
            product_id = re.findall(r'/item/(\d+)\.html', link)
            p_details = aliexpress.get_products_details([product_id[0]]) if product_id else None
            
            if p_details:
                title = p_details[0].product_title
                price = p_details[0].target_sale_price
                img = p_details[0].product_main_image_url
                
                bot.delete_message(message.chat.id, message_id)
                bot.send_photo(message.chat.id, img, caption=f"🛒 المنتج: {title}\n💰 السعر: {price} $\n\n🔗 الرابط: {affiliate_link}", reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, f"🔗 الرابط جاهز: {affiliate_link}", reply_markup=keyboard)
        except:
            bot.send_message(message.chat.id, f"🔗 الرابط جاهز: {affiliate_link}", reply_markup=keyboard)
    except:
        bot.send_message(message.chat.id, "حدث خطأ أثناء معالجة الرابط 🤷🏻‍♂️")

def extract_link(text):
    link_pattern = r'https?://\S+|www\.\S+'
    links = re.findall(link_pattern)
    return links[0] if links else None

@bot.message_handler(func=lambda message: True)
def get_
