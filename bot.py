import os
import logging
import json
import asyncio
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

BOT_TOKEN    = os.getenv("BOT_TOKEN", "8635217482:AAEkjYMV1qzzA6_1hEsTmhpyGlgpoS7J2XA")
ADMIN_ID     = int(os.getenv("ADMIN_ID", "6417175819"))
ADMIN_ID2    = int(os.getenv("ADMIN_ID2", "5345513906"))
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://shadmanovad7-star.github.io/xonhalol/")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

SELECT_LANG, MAIN_MENU, GET_NAME, GET_PHONE, GET_ADDRESS, GET_PAYMENT, CONFIRM_ORDER = range(7)

T = {
    "uz": {
        "welcome": "Tilni tanlang:",
        "main_menu": "Xush kelibsiz! 😊",
        "btn_products": "🛍 Mahsulotlar",
        "btn_orders": "📦 Buyurtmalarim",
        "btn_contact": "☎️ Aloqa",
        "open_app": "👇 Do'konni ochish uchun bosing:",
        "open_btn": "🛍 Do'konni ochish",
        "enter_name": "📝 Ismingizni kiriting:",
        "enter_phone": "📱 Telefon raqamingizni yuboring:",
        "send_contact": "📲 Kontakt yuborish",
        "enter_address": "📍 Manzilingizni yuboring:",
        "send_location": "📍 Lokatsiya yuborish",
        "write_manual": "✍️ Qo'lda yozish",
        "select_pay": "💳 To'lov turini tanlang:",
        "pay_click": "💳 Click",
        "pay_payme": "💰 Payme",
        "pay_cash": "💵 Naqd pul",
        "confirm_btn": "✅ Tasdiqlash",
        "cancel_btn": "❌ Bekor qilish",
        "cancelled": "❌ Buyurtma bekor qilindi.",
        "no_orders": "📦 Hozircha buyurtmalaringiz yo'q.",
        "contact_text": "☎️ Aloqa:\n\n📞 Tel: +998 97 734 75 72",
        "order_success": lambda oid: (
            f"✅ Buyurtmangiz qabul qilindi!\n\n"
            f"📦 Buyurtma raqami: #{oid}\n\n"
            f"🕒 Buyurtmangiz qachon yetkazib berilishi haqida\n"
            f"siz bilan tez orada operatorlarimiz bog'lanishadi.\n\n"
            f"🙏 Xaridingiz uchun rahmat!"
        ),
        "status": {
            "accepted": "✅ Buyurtmangiz qabul qilindi! Tayyorlanmoqda...",
            "shipped": "🚚 Kuryer yo'lga chiqdi!",
            "delivered": "✅ Buyurtmangiz yetkazildi! Rahmat!",
            "cancelled": "❌ Buyurtmangiz bekor qilindi.",
        },
    },
    "ru": {
        "welcome": "Выберите язык:",
        "main_menu": "Добро пожаловать! 😊",
        "btn_products": "🛍 Товары",
        "btn_orders": "📦 Мои заказы",
        "btn_contact": "☎️ Связь",
        "open_app": "👇 Нажмите чтобы открыть магазин:",
        "open_btn": "🛍 Открыть магазин",
        "enter_name": "📝 Введите ваше имя:",
        "enter_phone": "📱 Отправьте номер телефона:",
        "send_contact": "📲 Отправить контакт",
        "enter_address": "📍 Отправьте адрес доставки:",
        "send_location": "📍 Отправить геолокацию",
        "write_manual": "✍️ Написать вручную",
        "select_pay": "💳 Выберите способ оплаты:",
        "pay_click": "💳 Click",
        "pay_payme": "💰 Payme",
        "pay_cash": "💵 Наличные",
        "confirm_btn": "✅ Подтвердить",
        "cancel_btn": "❌ Отменить",
        "cancelled": "❌ Заказ отменён.",
        "no_orders": "📦 У вас пока нет заказов.",
        "contact_text": "☎️ Для связи:\n\n📞 Тел: +998 97 734 75 72",
        "order_success": lambda oid: (
            f"✅ Ваш заказ принят!\n\n"
            f"📦 Номер заказа: #{oid}\n\n"
            f"🕒 Наши операторы свяжутся с вами\n"
            f"в ближайшее время насчёт доставки.\n\n"
            f"🙏 Спасибо за покупку!"
        ),
        "status": {
            "accepted": "✅ Заказ принят! Готовится...",
            "shipped": "🚚 Курьер уже в пути!",
            "delivered": "✅ Заказ доставлен! Спасибо!",
            "cancelled": "❌ Ваш заказ отменён.",
        },
    }
}

user_store = {}
order_store = {}
order_cnt = [1000]

def get_lang(uid): return user_store.get(uid, {}).get("lang", "uz")
def tx(uid, key): return T[get_lang(uid)][key]
def new_oid(): order_cnt[0] += 1; return order_cnt[0]

def main_kb(uid):
    lang = get_lang(uid)
    return ReplyKeyboardMarkup([
        [KeyboardButton(T[lang]["btn_products"])],
        [KeyboardButton(T[lang]["btn_orders"])],
        [KeyboardButton(T[lang]["btn_contact"])],
    ], resize_keyboard=True)

async def go_main(msg, uid, context):
    lang = get_lang(uid)
    await msg.reply_text(T[lang]["main_menu"], reply_markup=main_kb(uid))
    return MAIN_MENU

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_store.setdefault(uid, {})
    
    args = context.args
    if args and args[0].startswith('c_'):
        try:
            from urllib.parse import unquote
            parts = args[0][2:].split('|')
            lines = []
            total = 0
            cart_list = []
            for p in parts:
                seg = p.split('~')
                if len(seg) == 3:
                    name = unquote(seg[0])
                    qty = int(seg[1])
                    price = int(seg[2])
                    total += price * qty
                    lines.append(f"• {name} x{qty} = {price*qty:,} som")
                    cart_list.append({'name': name, 'qty': qty, 'price': price})
            user_store[uid]['cart'] = cart_list
            user_store[uid]['cart_text'] = '\n'.join(lines)
            user_store[uid]['cart_total'] = total
            lang = get_lang(uid)
            if lang == 'uz':
                msg = "🛒 Savatdagi mahsulotlar:\n\n" + '\n'.join(lines) + f"\n\n💵 Jami: {total:,} so'm\n\n📝 Ismingizni kiriting:"
            else:
                msg = "🛒 Товары в корзине:\n\n" + '\n'.join(lines) + f"\n\n💵 Итого: {total:,} сум\n\n📝 Введите ваше имя:"
            await update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())
            return GET_NAME
        except Exception as e:
            pass

    await update.message.reply_text(
        "🍽 Muzlatilgan mazali taomlar\n🏠 Uy ta'mini eslatuvchi lazzat\n🕐 Buyurtmalar 24/7"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский язык", callback_data="lang_ru"),
    ]])
    await update.message.reply_text(T["uz"]["welcome"], reply_markup=kb)
    return SELECT_LANG

async def cb_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    lang = "uz" if q.data == "lang_uz" else "ru"
    user_store.setdefault(uid, {})["lang"] = lang
    await q.message.reply_text(T[lang]["main_menu"], reply_markup=main_kb(uid))
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    text = update.message.text
    if text == T[lang]["btn_products"]:
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton(T[lang]["open_btn"], web_app=WebAppInfo(url=MINI_APP_URL))
        ]])
        await update.message.reply_text(T[lang]["open_app"], reply_markup=kb)
    elif text == T[lang]["btn_orders"]:
        orders = [o for o in order_store.values() if o["uid"] == uid]
        if not orders:
            await update.message.reply_text(T[lang]["no_orders"])
        else:
            icons = {"pending":"🕒","accepted":"✅","shipped":"🚚","delivered":"✅","cancelled":"❌"}
            msg = "📦 Buyurtmalaringiz:\n\n" if lang=="uz" else "📦 Ваши заказы:\n\n"
            for o in orders[-5:]:
                msg += f"{icons.get(o['status'],'🕒')} #{o['oid']} — {o['total']:,} so'm\n"
            await update.message.reply_text(msg)
    elif text == T[lang]["btn_contact"]:
        await update.message.reply_text(T[lang]["contact_text"])
    return MAIN_MENU

async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    log.info(f"WebApp data from {uid}")
    try:
        data = json.loads(update.message.web_app_data.data)
        log.info(f"Action: {data.get('action')}, items: {len(data.get('cart',[]))}")
    except Exception as e:
        log.error(f"WebApp parse error: {e}")
        return MAIN_MENU

    if data.get("action") == "checkout":
        cart = data.get("cart", [])
        user_store.setdefault(uid, {})["cart"] = cart
        user_store[uid]["cart_text"] = '\n'.join([f"• {i['name']} × {i['qty']} = {i['price']*i['qty']:,} so'm" for i in cart])
        await update.message.reply_text(
            tx(uid, "enter_name"),
            reply_markup=ReplyKeyboardRemove()
        )
        return GET_NAME
    return MAIN_MENU

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.message.text.strip()
    user_store[uid]["name"] = name
    lang = get_lang(uid)
    kb = ReplyKeyboardMarkup([[KeyboardButton(T[lang]["send_contact"], request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(T[lang]["enter_phone"], reply_markup=kb)
    return GET_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    phone = update.message.contact.phone_number if update.message.contact else update.message.text
    if not phone.startswith("+"): phone = "+" + phone
    user_store[uid]["phone"] = phone
    loc_btn = KeyboardButton(T[lang]["send_location"], request_location=True)
    man_btn = KeyboardButton(T[lang]["write_manual"])
    kb = ReplyKeyboardMarkup([[loc_btn],[man_btn]], resize_keyboard=True)
    await update.message.reply_text(T[lang]["enter_address"], reply_markup=kb)
    return GET_ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    if update.message.location:
        loc = update.message.location
        address = f"📍 {loc.latitude:.5f}, {loc.longitude:.5f}"
    else:
        address = update.message.text.strip()
    user_store[uid]["address"] = address
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(T[lang]["pay_click"], callback_data="pay_click")],
        [InlineKeyboardButton(T[lang]["pay_payme"], callback_data="pay_payme")],
        [InlineKeyboardButton(T[lang]["pay_cash"], callback_data="pay_cash")],
    ])
    await update.message.reply_text(T[lang]["select_pay"], reply_markup=kb)
    return GET_PAYMENT

async def get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    lang = get_lang(uid)
    pay_map = {
        "pay_click": "Click 💳",
        "pay_payme": "Payme 💰",
        "pay_cash": "Naqd 💵" if lang=="uz" else "Наличные 💵"
    }
    payment = pay_map.get(q.data, "Naqd")
    user_store[uid]["payment"] = payment

    if q.data == "pay_cash":
        msg = "✅ Yaxshi, hurmatli mijoz!\n\nBuyurtmangiz yetkazib berilgandan keyin naqd pul orqali to'lov qilishingiz mumkin. 💵" if lang=="uz" else "✅ Хорошо!\n\nВы оплатите наличными после доставки. 💵"
    else:
        msg = "✅ Yaxshi, hurmatli mijoz!\n\nKarta orqali to'lov uchun tez orada adminlarimiz siz bilan bog'lanishadi. 💳" if lang=="uz" else "✅ Хорошо!\n\nДля оплаты картой наш администратор свяжется с вами. 💳"
    await q.message.reply_text(msg)

    ud = user_store[uid]
    cart = ud.get("cart", [])
    cart_text = ud.get("cart_text", "")
    total = sum(i["price"]*i["qty"] for i in cart) if cart else 0
    user_store[uid]["total"] = total

    if lang == "uz":
        summary = (
            f"📋 Buyurtma:\n\n"
            f"👤 {ud.get('name','')}\n"
            f"📞 {ud.get('phone','')}\n"
            f"📍 {ud.get('address','')}\n"
            f"💳 {payment}\n\n"
            f"\U0001f6cd Mahsulotlar:\n{cart_text}\n\n"
            f"💵 Jami: {total:,} so'm"
        )
    else:
        summary = (
            f"📋 Заказ:\n\n"
            f"👤 {ud.get('name','')}\n"
            f"📞 {ud.get('phone','')}\n"
            f"📍 {ud.get('address','')}\n"
            f"💳 {payment}\n\n"
            f"🛍 Товары:\n{cart_text or 'Spisok pust'}\n\n"
            f"💵 Итого: {total:,} сум"
        )

    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(T[lang]["confirm_btn"], callback_data="order_confirm"),
        InlineKeyboardButton(T[lang]["cancel_btn"], callback_data="order_cancel"),
    ]])
    await q.message.reply_text(summary, reply_markup=kb)
    return CONFIRM_ORDER

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    lang = get_lang(uid)
    if q.data == "order_cancel":
        await q.message.reply_text(T[lang]["cancelled"])
        return await go_main(q.message, uid, context)
    
    oid = new_oid()
    ud = user_store[uid]
    order = {
        "oid": oid, "uid": uid, "lang": lang,
        "name": ud.get("name"), "phone": ud.get("phone"),
        "address": ud.get("address"), "payment": ud.get("payment"),
        "cart": ud.get("cart", []),
        "cart_text": ud.get("cart_text", ""),
        "total": ud.get("total", 0),
        "status": "pending",
        "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "tg_name": q.from_user.full_name,
        "tg_username": q.from_user.username or "yo'q",
    }
    order_store[oid] = order
    await q.message.reply_text(T[lang]["order_success"](oid))
    await notify_admins(context, order)
    return await go_main(q.message, uid, context)

async def notify_admins(context, order):
    cart_text = order.get("cart_text", "")
    if not cart_text:
        cart_text = '\n'.join([f"  • {i['name']} × {i['qty']} = {i['price']*i['qty']:,} so'm" for i in order.get("cart",[])])
    
    text = (
        f"🆕 YANGI BUYURTMA!\n\n"
        f"📦 #{order['oid']}\n"
        f"👤 Ism: {order['name']}\n"
        f"📞 Tel: {order['phone']}\n"
        f"📍 Manzil: {order['address']}\n"
        f"💳 To'lov: {order['payment']}\n"
        f"⏰ Vaqt: {order['created']}\n"
        f"👤 Telegram: {order['tg_name']}\n"
        f"🔗 @{order['tg_username']}\n"
        f"🆔 ID: {order['uid']}\n\n"
        f"🛍 Mahsulotlar:\n{cart_text}\n\n"
        f"💵 Jami: {order['total']:,} so'm"
    )
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Qabul", callback_data=f"adm_accept_{order['oid']}"),
            InlineKeyboardButton("🚚 Yuborildi", callback_data=f"adm_ship_{order['oid']}"),
        ],
        [
            InlineKeyboardButton("✅ Yetkazildi", callback_data=f"adm_deliver_{order['oid']}"),
            InlineKeyboardButton("❌ Bekor", callback_data=f"adm_cancel_{order['oid']}"),
        ],
    ])
    for adm in [ADMIN_ID, ADMIN_ID2]:
        try:
            await context.bot.send_message(chat_id=adm, text=text, reply_markup=kb)
        except Exception as e:
            log.error(f"Admin {adm}: {e}")

async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.split("_")
    action, oid = parts[1], int(parts[2])
    order = order_store.get(oid)
    if not order: return
    uid = order["uid"]
    lang = order.get("lang", "uz")
    status_map = {
        "accept": ("accepted", T[lang]["status"]["accepted"]),
        "ship": ("shipped", T[lang]["status"]["shipped"]),
        "deliver": ("delivered", T[lang]["status"]["delivered"]),
        "cancel": ("cancelled", T[lang]["status"]["cancelled"]),
    }
    if action in status_map:
        new_status, user_msg = status_map[action]
        order["status"] = new_status
        try:
            await context.bot.send_message(chat_id=uid, text=user_msg)
        except:
            pass
        labels = {
            "accepted": "✅ Qabul",
            "shipped": "🚚 Yuborildi",
            "delivered": "✅ Yetkazildi",
            "cancelled": "❌ Bekor"
        }
        try:
            await q.edit_message_text(
                q.message.text + f"\n\n{labels.get(new_status,'')} — {datetime.now().strftime('%H:%M')}",
                reply_markup=None
            )
        except:
            pass

async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    return await go_main(update.message, uid, context)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", cmd_start),
        ],
        states={
            SELECT_LANG: [CallbackQueryHandler(cb_lang, pattern="^lang_")],
            MAIN_MENU: [
                MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data),
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu),
            ],
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_PHONE: [
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone),
            ],
            GET_ADDRESS: [
                MessageHandler(filters.LOCATION, get_address),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_address),
            ],
            GET_PAYMENT: [CallbackQueryHandler(get_payment, pattern="^pay_")],
            CONFIRM_ORDER: [CallbackQueryHandler(confirm_order, pattern="^order_")],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
        allow_reentry=True,
    )

    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data), group=-1)
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_action, pattern="^adm_"))

    log.info("✅ Xon Halol bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
