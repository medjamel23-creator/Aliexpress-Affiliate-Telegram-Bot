#!/usr/bin/env python
# coding: utf-8



# In[1]:

import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import requests, json
from urllib.parse import urlparse, parse_qs

# In[2]:

bot = telebot.TeleBot('6613740819:AAEiGrOSCcuVNQTrzkhbJ4Bg29oBm6UU6nw')
  
aliexpress = AliexpressApi('502336', 'qW3MlLGKtt7jnZOg8KkHpfCbTaac2LOq',
                           models.Language.EN, models.Currency.EUR, 'default')
# In[3]:

keyboardStart = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton("⭐️ألعاب لجمع العملات المعدنية⭐️",
                                  callback_data="games")
btn2 = types.InlineKeyboardButton("⭐️تخفيض العملات على منتجات السلة 🛒⭐️",
                                  callback_data='click')

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("أحدث العروض 🔥", url="https://a.aliexpress.com/_mtV0j3")
    markup.add(btn1)


keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton("⭐️ألعاب لجمع العملات المعدنية⭐️",
                                  callback_data="games")
btn2 = types.InlineKeyboardButton("⭐️تخفيض العملات على منتجات السلة 🛒⭐️",
                                  callback_data='click')
btn3 = types.InlineKeyboardButton("❤️ اشترك في القناة للمزيد من العروض ❤️",
                                  url="https://t.me/AliXPromotion")

keyboard.add(btn1, btn2, btn3)

keyboard_games = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(
    " ⭐️ صفحة مراجعة وجمع النقاط يوميا ⭐️",
    url="https://s.click.aliexpress.com/e/_on0MwkF")
btn2 = types.InlineKeyboardButton(
    "⭐️ لعبة Merge boss ⭐️", url="https://s.click.aliexpress.com/e/_DlCyg5Z")
btn3 = types.InlineKeyboardButton(
    "⭐️ لعبة Fantastic Farm ⭐️",
    url="https://s.click.aliexpress.com/e/_DBBkt9V")
btn4 = types.InlineKeyboardButton(
    "⭐️ لعبة قلب الاوراق Flip ⭐️",
    url="https://s.click.aliexpress.com/e/_DdcXZ2r")
btn5 = types.InlineKeyboardButton(
    "⭐️ لعبة GoGo Match ⭐️", url="https://s.click.aliexpress.com/e/_DDs7W5D")
keyboard_games.add(btn1, btn2, btn3, btn4, btn5)

# In[4]:


@bot.message_handler(commands=['start'])
def welcome_user(message):
  bot.send_message(
      message.chat.id,
      "مرحبا بك، ارسل لنا رابط المنتج الذي تريد شرائه لنوفر لك افضل سعر له 👌 \n",
      reply_markup=keyboardStart)


@bot.callback_query_handler(func=lambda call: call.data == 'click')
def button_click(callback_query):
  bot.edit_message_text(chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text="...")

  # Send a message with text
  #bot.send_message(callback_query.message.chat.id, "This is the message text.")

  text = "✅1-ادخل الى السلة من هنا:\n" \
         " https://s.click.aliexpress.com/e/_opGCtMf \n" \
         "✅2-قم باختيار المنتجات التي تريد تخفيض سعرها\n" \
         "✅3-اضغط على زر دفع ليحولك لصفحة التأكيد \n" \
         "✅4-اضغط على الايقونة في الاعلى وانسخ الرابط  هنا في البوت لتتحصل على رابط التخفيض"

  img_link1 = "https://i.postimg.cc/HkMxWS1T/photo-5893070682508606111-y.jpg"
  bot.send_photo(callback_query.message.chat.id,
                 img_link1,
                 caption=text,
                 reply_markup=keyboard)


# In[5]:


def get_affiliate_links(message, message_id, link):
  try:

  
    limit_links = aliexpress.get_affiliate_links(
        f'https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl={link}?sourceType=561&aff_fcid='
    )
    limit_links = limit_links[0].promotion_link

    try:
      img_link = aliexpress.get_products_details([
          '1000006468625',
          f'https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl={link}'
      ])
      price_pro = img_link[0].target.sale_price
      title_link = img_link[0].product_title
      img_link = img_link[0].product_main_image_url
      print(img_link)
      bot.delete_message(message.chat.id, message_id)
      bot.send_photo(message.chat.id,
                     img_link,
                     caption=" \n🛒 منتجك هو  : 🔥 \n"
                     f" {title_link} 🛍 \n"
                     f"  سعر المنتج  : "
                     f" {price_pro}  دولار 💵\n"
                     " \n قارن بين الاسعار واشتري 🔥 \n"
                     "💰 عرض العملات (السعر النهائي عند الدفع)  : \n"
                     f"الرابط {affiliate_link} \n"
                     f"💎 عرض السوبر  : \n"
                     f"الرابط {super_links} \n"
                     f"♨️ عرض محدود  : \n"
                     f"الرابط {limit_links} \n\n"
                     "#AliXPromotion ✅",
                     reply_markup=keyboard)

    except:

      bot.delete_message(message.chat.id, message_id)
      bot.send_message(message.chat.id, "قارن بين الاسعار واشتري 🔥 \n"
                       "💰 عرض العملات (السعر النهائي عند الدفع) : \n"
                       f"الرابط {affiliate_link} \n"
                       f"💎 عرض السوبر : \n"
                       f"الرابط {super_links} \n"
                       f"♨️ عرض محدود : \n"
                       f"الرابط {limit_links} \n\n"
                       "#AliXPromotion ✅",
                       reply_markup=keyboard)

  except:
    bot.send_message(message.chat.id, "حدث خطأ 🤷🏻‍♂️")


# In[6]:
def extract_link(text):
  # Regular expression pattern to match links
  link_pattern = r'https?://\S+|www\.\S+'

  # Find all occurrences of the pattern in the text
  links = re.findall(link_pattern)

  if links:
    return links[0]


def build_shopcart_link(link):
  params = get_url_params(link)
  shop_cart_link = "https://www.aliexpress.com/p/trade/confirm.html?"
  shop_cart_params = {
      "availableProductShopcartIds":
      ",".join(params["availableProductShopcartIds"]),
      "extraParams":
      json.dumps({"channelInfo": {
          "sourceType": "620"
      }}, separators=(',', ':'))
  }
  return create_query_string_url(link=shop_cart_link, params=shop_cart_params)


def get_url_params(link):
  parsed_url = urlparse(link)
  params = parse_qs(parsed_url.query)
  return params


def create_query_string_url(link, params):
  return link + urllib.parse.urlencode(params)


## Shop cart Affiliate تخفيض السلة
def get_affiliate_shopcart_link(link, message):
  try:
    shopcart_link = build_shopcart_link(link)
    affiliate_link = aliexpress.get_affiliate_links(
        shopcart_link)[0].promotion_link

    text2 = f"هذا رابط تخفيض السلة \n" \
           f"{str(affiliate_link)}" \

    img_link3 = "https://i.postimg.cc/HkMxWS1T/photo-5893070682508606111-y.jpg"
    bot.send_photo(message.chat.id, img_link3, caption=text2)

  except:
    bot.send_message(message.id, "حدث خطأ 🤷🏻‍♂️")


@bot.message_handler(func=lambda message: True)
def get_link(message):
  link = extract_link(message.text)

  sent_message = bot.send_message(message.chat.id,
                                  'المرجو الانتظار قليلا، يتم تجهيز العروض ⏳')
  message_id = sent_message.message_id
  if link and "aliexpress.com" in link and not ("p/shoppingcart"
                                                in message.text.lower()):
    if "availableProductShopcartIds".lower() in message.text.lower():
      get_affiliate_shopcart_link(link, message)
      return
    get_affiliate_links(message, message_id, link)

  else:
    bot.delete_message(message.chat.id, message_id)
    bot.send_message(message.chat.id,
                     "الرابط غير صحيح ! تأكد من رابط المنتج أو اعد المحاولة.\n"
                     " قم بإرسال <b> الرابط فقط</b> بدون عنوان المنتج",
                     parse_mode='HTML')


# In[7]:


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
  bot.send_message(call.message.chat.id, "..")

  img_link2 = "https://i.postimg.cc/zvDbVTS0/photo-5893070682508606110-x.jpg"
  bot.send_photo(
      call.message.chat.id,
      img_link2,
      caption=
      "روابط ألعاب جمع العملات المعدنية لإستعمالها في خفض السعر لبعض المنتجات، قم بالدخول يوميا لها للحصول على أكبر عدد ممكن في اليوم 👇",
      reply_markup=keyboard_games)

  # In[ ]:


keep_alive()

infinity_polling(timeout=10, long_polling_timeout=5)
