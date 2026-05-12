"""
╔══════════════════════════════════════════════╗
║     XON HALOL - TO'LIQ TELEGRAM BOT         ║
║     Python 3.10+ | python-telegram-bot 20.x ║
╚══════════════════════════════════════════════╝

O'rnatish:
  pip install python-telegram-bot==20.7

Ishga tushirish:
  python xonhalol_bot.py
"""

import logging
import json
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    WebAppInfo
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ─────────────────────────────────────────────
#  ⚙️  SOZLAMALAR — BULARNI TO'LDIRING
# ─────────────────────────────────────────────
BOT_TOKEN    = "YOUR_BOT_TOKEN"          # @BotFather dan oling
ADMIN_ID     = 123456789                 # @userinfobot dan oling (int)
MINI_APP_URL = "https://YOUR_SITE/xonhalol_final.html"  # Deploy qilgan URL

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  CONVERSATION STATES
# ─────────────────────────────────────────────
(
    SELECT_LANG,
    MAIN_MENU,
    GET_NAME,
    GET_PHONE,
    GET_ADDRESS,
    GET_PAYMENT,
    CONFIRM_ORDER,
) = range(7)

# ─────────────────────────────────────────────
#  MATNLAR (UZ / RU)
# ─────────────────────────────────────────────
T = {
    "uz": {
        "welcome":      "Assalomu alaykum! 👋\nO'zingizga qulay bo'lgan tilni tanlang:",
        "main_menu":    "Xush kelibsiz! 😊\nKerakli bo'limni tanlang:",
        "btn_products": "🛍 Mahsulotlar",
        "btn_orders":   "📦 Buyurtmalarim",
        "btn_contact":  "☎️ Aloqa",
        "open_app":     "👇 Mahsulotlarni ko'rish uchun tugmani bosing:",
        "open_btn":     "🛍 Do'konni ochish",
        "enter_name":   "📝 Ismingizni kiriting:",
        "enter_phone":  "📱 Telefon raqamingizni yuboring:",
        "send_contact": "📲 Kontakt yuborish",
        "enter_address":"📍 Yetkazib berish manzilini yuboring:\n\n📍 Lokatsiya yuboring  yoki\n✍️ Manzilni yozing",
        "send_location":"📍 Lokatsiya yuborish",
        "write_manual": "✍️ Qo'lda yozish",
        "select_pay":   "💳 To'lov turini tanlang:",
        "pay_click":    "💳 Click",
        "pay_payme":    "💰 Payme",
        "pay_cash":     "💵 Naqd pul",
        "confirm_btn":  "✅ Tasdiqlash",
        "cancel_btn":   "❌ Bekor qilish",
        "cancelled":    "❌ Buyurtma bekor qilindi.",
        "no_orders":    "📦 Hozircha buyurtmalaringiz yo'q.",
        "orders_title": "📦 Sizning buyurtmalaringiz:\n\n",
        "contact_text": "☎️ Aloqa uchun:\n\n📞 Tel: +998 97 734 75 72\n💬 Telegram: @xonhalol",
        "order_success": lambda oid: (
            f"✅ Buyurtmangiz qabul qilindi!\n\n"
            f"📦 Buyurtma raqami: #{oid}\n"
            f"🕒 Yetkazish vaqti: bugun yoki ertaga\n"
            f"📞 Iltimos aloqada bo'ling\n"
            f"🙏 Xaridingiz uchun rahmat!"
        ),
        "status": {
            "accepted":  "✅ Buyurtmangiz qabul qilindi!\n👨‍🍳 Tayyorlanmoqda...",
            "shipped":   "🚚 Kuryer yo'lga chiqdi!\nYaqinda yetib boradi 😊",
            "delivered": "✅ Buyurtmangiz yetkazildi!\n🙏 Rahmat, yana keling!",
            "cancelled": "❌ Buyurtmangiz bekor qilindi.\nSavollar: @xonhalol",
        },
    },
    "ru": {
        "welcome":      "Привет! 👋\nВыберите удобный язык:",
        "main_menu":    "Добро пожаловать! 😊\nВыберите раздел:",
        "btn_products": "🛍 Товары",
        "btn_orders":   "📦 Мои заказы",
        "btn_contact":  "☎️ Связь",
        "open_app":     "👇 Нажмите кнопку для просмотра товаров:",
        "open_btn":     "🛍 Открыть магазин",
        "enter_name":   "📝 Введите ваше имя:",
        "enter_phone":  "📱 Отправьте номер телефона:",
        "send_contact": "📲 Отправить контакт",
        "enter_address":"📍 Отправьте адрес доставки:\n\n📍 Отправить геолокацию  или\n✍️ Написать адрес",
        "send_location":"📍 Отправить геолокацию",
        "write_manual": "✍️ Написать вручную",
        "select_pay":   "💳 Выберите способ оплаты:",
        "pay_click":    "💳 Click",
        "pay_payme":    "💰 Payme",
        "pay_cash":     "💵 Наличные",
        "confirm_btn":  "✅ Подтвердить",
        "cancel_btn":   "❌ Отменить",
        "cancelled":    "❌ Заказ отменён.",
        "no_orders":    "📦 У вас пока нет заказов.",
        "orders_title": "📦 Ваши заказы:\n\n",
        "contact_text": "☎️ Для связи:\n\n📞 Тел: +998 97 734 75 72\n💬 Telegram: @xonhalol",
        "order_success": lambda oid: (
            f"✅ Ваш заказ принят!\n\n"
            f"📦 Номер заказа: #{oid}\n"
            f"🕒 Доставка: сегодня или завтра\n"
            f"📞 Пожалуйста, оставайтесь на связи\n"
            f"🙏 Спасибо за покупку!"
        ),
        "status": {
            "accepted":  "✅ Ваш заказ принят!\n👨‍🍳 Готовится...",
            "shipped":   "🚚 Курьер уже в пути!\nСкоро будет у вас 😊",
            "delivered": "✅ Заказ доставлен!\n🙏 Спасибо, приходите ещё!",
            "cancelled": "❌ Ваш заказ отменён.\nВопросы: @xonhalol",
        },
    },
}

# ─────────────────────────────────────────────
#  IN-MEMORY STORAGE
# ─────────────────────────────────────────────
user_store  = {}   # {user_id: {"lang", "name", "phone", "address", "payment", "cart"}}
order_store = {}   # {order_id: order_dict}
order_cnt   = [1000]

def get_lang(uid):
    return user_store.get(uid, {}).get("lang", "uz")

def tx(uid, key):
    return T[get_lang(uid)][key]

def new_order_id():
    order_cnt[0] += 1
    return order_cnt[0]

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def main_menu_keyboard(uid):
    lang = get_lang(uid)
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(T[lang]["btn_products"])],
            [KeyboardButton(T[lang]["btn_orders"])],
            [KeyboardButton(T[lang]["btn_contact"])],
        ],
        resize_keyboard=True,
    )

async def send_main_menu(update_or_msg, uid, context, text=None):
    """ReplyKeyboard bilan asosiy menyu yuboradi."""
    lang = get_lang(uid)
    msg_text = text or T[lang]["main_menu"]
    kb = main_menu_keyboard(uid)
    if hasattr(update_or_msg, "message"):
        await update_or_msg.message.reply_text(msg_text, reply_markup=kb)
    else:
        await update_or_msg.reply_text(msg_text, reply_markup=kb)
    return MAIN_MENU

# ─────────────────────────────────────────────
#  /start
# ─────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_store.setdefault(uid, {})

    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский язык", callback_data="lang_ru"),
    ]])
    await update.message.reply_text(
        T["uz"]["welcome"],
        reply_markup=kb
    )
    return SELECT_LANG

# ─────────────────────────────────────────────
#  TIL TANLASH
# ─────────────────────────────────────────────
async def cb_select_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid   = query.from_user.id
    lang  = "uz" if query.data == "lang_uz" else "ru"
    user_store.setdefault(uid, {})["lang"] = lang

    await query.message.reply_text(
        T[lang]["main_menu"],
        reply_markup=main_menu_keyboard(uid)
    )
    return MAIN_MENU

# ─────────────────────────────────────────────
#  ASOSIY MENYU
# ─────────────────────────────────────────────
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    lang = get_lang(uid)
    text = update.message.text

    if text == T[lang]["btn_products"]:
        # Mini App tugmasi
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                T[lang]["open_btn"],
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]])
        await update.message.reply_text(
            T[lang]["open_app"],
            reply_markup=kb
        )

    elif text == T[lang]["btn_orders"]:
        user_orders = [o for o in order_store.values() if o["user_id"] == uid]
        if not user_orders:
            await update.message.reply_text(T[lang]["no_orders"])
        else:
            status_icons = {
                "pending":   "🕒", "accepted": "✅",
                "shipped":   "🚚", "delivered":"✅", "cancelled":"❌"
            }
            msg = T[lang]["orders_title"]
            for o in user_orders[-10:]:
                ic = status_icons.get(o["status"], "🕒")
                msg += f"{ic} #{o['order_id']} — {o['total']:,} so'm\n"
            await update.message.reply_text(msg)

    elif text == T[lang]["btn_contact"]:
        await update.message.reply_text(T[lang]["contact_text"])

    return MAIN_MENU

# ─────────────────────────────────────────────
#  MINI APP DAN KELGAN DATA (checkout bosilganda)
# ─────────────────────────────────────────────
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    try:
        data = json.loads(update.message.web_app_data.data)
    except Exception:
        return MAIN_MENU

    if data.get("action") == "checkout":
        cart = data.get("cart", [])
        user_store.setdefault(uid, {})["cart"] = cart
        lang = get_lang(uid)

        await update.message.reply_text(
            tx(uid, "enter_name"),
            reply_markup=ReplyKeyboardRemove()
        )
        return GET_NAME

    return MAIN_MENU

# ─────────────────────────────────────────────
#  CHECKOUT — QADAM 1: ISM
# ─────────────────────────────────────────────
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text(tx(uid, "enter_name"))
        return GET_NAME

    user_store[uid]["name"] = name
    lang = get_lang(uid)

    contact_btn = KeyboardButton(T[lang]["send_contact"], request_contact=True)
    kb = ReplyKeyboardMarkup([[contact_btn]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(T[lang]["enter_phone"], reply_markup=kb)
    return GET_PHONE

# ─────────────────────────────────────────────
#  CHECKOUT — QADAM 2: TELEFON
# ─────────────────────────────────────────────
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if update.message.contact:
        phone = update.message.contact.phone_number
        if not phone.startswith("+"):
            phone = "+" + phone
    else:
        phone = update.message.text.strip()

    user_store[uid]["phone"] = phone
    lang = get_lang(uid)

    loc_btn = KeyboardButton(T[lang]["send_location"], request_location=True)
    man_btn = KeyboardButton(T[lang]["write_manual"])
    kb = ReplyKeyboardMarkup([[loc_btn], [man_btn]], resize_keyboard=True)
    await update.message.reply_text(T[lang]["enter_address"], reply_markup=kb)
    return GET_ADDRESS

# ─────────────────────────────────────────────
#  CHECKOUT — QADAM 3: MANZIL
# ─────────────────────────────────────────────
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if update.message.location:
        loc = update.message.location
        address = f"📍 {loc.latitude:.5f}, {loc.longitude:.5f}"
    else:
        address = update.message.text.strip()

    user_store[uid]["address"] = address
    lang = get_lang(uid)

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(T[lang]["pay_click"], callback_data="pay_click")],
        [InlineKeyboardButton(T[lang]["pay_payme"], callback_data="pay_payme")],
        [InlineKeyboardButton(T[lang]["pay_cash"],  callback_data="pay_cash")],
    ])
    await update.message.reply_text(
        T[lang]["select_pay"],
        reply_markup=kb
    )
    return GET_PAYMENT

# ─────────────────────────────────────────────
#  CHECKOUT — QADAM 4: TO'LOV
# ─────────────────────────────────────────────
async def get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid  = query.from_user.id
    lang = get_lang(uid)

    pay_map = {
        "pay_click": "Click 💳",
        "pay_payme": "Payme 💰",
        "pay_cash":  "Naqd 💵" if lang == "uz" else "Наличные 💵",
    }
    payment = pay_map.get(query.data, "Naqd")
    user_store[uid]["payment"] = payment

    ud    = user_store[uid]
    cart  = ud.get("cart", [])
    items = ""
    sub   = 0
    for item in cart:
        line = item["price"] * item["qty"]
        sub += line
        items += f"  • {item['name']} × {item['qty']} = {line:,} so'm\n"

    delivery   = 10_000
    grand      = sub + delivery
    user_store[uid]["total"]    = grand
    user_store[uid]["delivery"] = delivery

    if lang == "uz":
        summary = (
            f"📋 Buyurtma ma'lumotlari:\n\n"
            f"👤 Ism: {ud.get('name')}\n"
            f"📞 Telefon: {ud.get('phone')}\n"
            f"📍 Manzil: {ud.get('address')}\n"
            f"💳 To'lov: {payment}\n\n"
            f"🛍 Mahsulotlar:\n{items}\n"
            f"💰 Mahsulotlar: {sub:,} so'm\n"
            f"🚚 Yetkazish: {delivery:,} so'm\n"
            f"💵 Jami: {grand:,} so'm"
        )
    else:
        summary = (
            f"📋 Данные заказа:\n\n"
            f"👤 Имя: {ud.get('name')}\n"
            f"📞 Телефон: {ud.get('phone')}\n"
            f"📍 Адрес: {ud.get('address')}\n"
            f"💳 Оплата: {payment}\n\n"
            f"🛍 Товары:\n{items}\n"
            f"💰 Товары: {sub:,} сум\n"
            f"🚚 Доставка: {delivery:,} сум\n"
            f"💵 Итого: {grand:,} сум"
        )

    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(T[lang]["confirm_btn"], callback_data="order_confirm"),
        InlineKeyboardButton(T[lang]["cancel_btn"],  callback_data="order_cancel"),
    ]])
    await query.message.reply_text(summary, reply_markup=kb)
    return CONFIRM_ORDER

# ─────────────────────────────────────────────
#  CHECKOUT — TASDIQLASH
# ─────────────────────────────────────────────
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid  = query.from_user.id
    lang = get_lang(uid)

    if query.data == "order_cancel":
        await query.message.reply_text(T[lang]["cancelled"])
        return await send_main_menu(query.message, uid, context)

    oid = new_order_id()
    ud  = user_store[uid]
    order = {
        "order_id": oid,
        "user_id":  uid,
        "lang":     lang,
        "name":     ud.get("name"),
        "phone":    ud.get("phone"),
        "address":  ud.get("address"),
        "payment":  ud.get("payment"),
        "cart":     ud.get("cart", []),
        "total":    ud.get("total"),
        "delivery": ud.get("delivery"),
        "status":   "pending",
        "created":  datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    order_store[oid] = order

    # Foydalanuvchiga
    success_text = T[lang]["order_success"](oid)
    await query.message.reply_text(success_text)

    # Adminga
    await notify_admin(context, order)

    return await send_main_menu(query.message, uid, context)

# ─────────────────────────────────────────────
#  ADMIN NOTIFICATION
# ─────────────────────────────────────────────
async def notify_admin(context, order):
    items = ""
    for it in order["cart"]:
        line = it["price"] * it["qty"]
        items += f"  • {it['name']} × {it['qty']} = {line:,} so'm\n"

    text = (
        f"🆕 YANGI BUYURTMA!\n\n"
        f"📦 ID: #{order['order_id']}\n"
        f"👤 Ism: {order['name']}\n"
        f"📞 Tel: {order['phone']}\n"
        f"📍 Manzil: {order['address']}\n"
        f"💳 To'lov: {order['payment']}\n"
        f"⏰ Vaqt: {order['created']}\n\n"
        f"🛍 Mahsulotlar:\n{items}\n"
        f"🚚 Yetkazish: {order['delivery']:,} so'm\n"
        f"💵 Jami: {order['total']:,} so'm"
    )

    oid = order["order_id"]
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Qabul",    callback_data=f"adm_accept_{oid}"),
            InlineKeyboardButton("🚚 Yuborildi", callback_data=f"adm_ship_{oid}"),
        ],
        [
            InlineKeyboardButton("✅ Yetkazildi", callback_data=f"adm_deliver_{oid}"),
            InlineKeyboardButton("❌ Bekor",      callback_data=f"adm_cancel_{oid}"),
        ],
    ])
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text,
            reply_markup=kb
        )
    except Exception as e:
        log.error(f"Admin xabari yuborilmadi: {e}")

# ─────────────────────────────────────────────
#  ADMIN ACTIONS (status o'zgartirish)
# ─────────────────────────────────────────────
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts  = query.data.split("_")
    action = parts[1]
    oid    = int(parts[2])

    order = order_store.get(oid)
    if not order:
        await query.answer("Buyurtma topilmadi!", show_alert=True)
        return

    uid  = order["user_id"]
    lang = order.get("lang", "uz")

    action_map = {
        "accept":  ("accepted",  T[lang]["status"]["accepted"]),
        "ship":    ("shipped",   T[lang]["status"]["shipped"]),
        "deliver": ("delivered", T[lang]["status"]["delivered"]),
        "cancel":  ("cancelled", T[lang]["status"]["cancelled"]),
    }

    if action not in action_map:
        return

    new_status, user_msg = action_map[action]
    order["status"] = new_status
    order_store[oid] = order

    # Foydalanuvchiga xabar
    try:
        await context.bot.send_message(chat_id=uid, text=user_msg)
    except Exception as e:
        log.error(f"User xabari yuborilmadi: {e}")

    # Admin xabarini yangilash
    status_labels = {
        "accepted":  "✅ Qabul qilindi",
        "shipped":   "🚚 Yuborildi",
        "delivered": "✅ Yetkazildi",
        "cancelled": "❌ Bekor qilindi",
    }
    label = status_labels.get(new_status, "")
    try:
        await query.edit_message_text(
            query.message.text + f"\n\n{label} — {datetime.now().strftime('%H:%M')}",
            reply_markup=None
        )
    except Exception:
        pass

# ─────────────────────────────────────────────
#  /cancel
# ─────────────────────────────────────────────
async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    return await send_main_menu(update.message, uid, context)

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            SELECT_LANG: [
                CallbackQueryHandler(cb_select_lang, pattern="^lang_"),
            ],
            MAIN_MENU: [
                MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data),
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler),
            ],
            GET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name),
            ],
            GET_PHONE: [
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone),
            ],
            GET_ADDRESS: [
                MessageHandler(filters.LOCATION, get_address),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_address),
            ],
            GET_PAYMENT: [
                CallbackQueryHandler(get_payment, pattern="^pay_"),
            ],
            CONFIRM_ORDER: [
                CallbackQueryHandler(confirm_order, pattern="^order_"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_action, pattern="^adm_"))

    log.info("✅ Xon Halol bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
