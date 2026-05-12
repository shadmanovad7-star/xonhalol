# 🚀 XON HALOL BOT — TO'LIQ O'RNATISH QO'LLANMASI

---

## 📁 KERAKLI FAYLLAR

```
xonhalol/
├── xonhalol_bot.py          ← Bot kodi
├── xonhalol_final.html      ← Mini App
└── requirements.txt
```

**requirements.txt:**
```
python-telegram-bot==20.7
```

---

## 1️⃣ BOT TOKEN OLISH (@BotFather)

1. Telegramda **@BotFather** ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting: masalan `Xon Halol`
4. Username kiriting: masalan `xonhalol_bot`
5. BotFather sizga **TOKEN** beradi:
   ```
   1234567890:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
6. Bu tokenni `xonhalol_bot.py` dagi:
   ```python
   BOT_TOKEN = "1234567890:AAFxxxxx..."
   ```
   ga qo'ying

---

## 2️⃣ ADMIN ID OLISH (@userinfobot)

1. Telegramda **@userinfobot** ga `/start` yuboring
2. U sizga `Id: 123456789` ko'rinishida ID beradi
3. Uni `xonhalol_bot.py` dagi:
   ```python
   ADMIN_ID = 123456789
   ```
   ga qo'ying

---

## 3️⃣ MINI APP NI INTERNET GA JOYLASHTIRISH

> ⚠️ Telegram Mini App faqat **HTTPS** da ishlaydi!
> Oddiy fayldan ishlamaydi — internet da joylash kerak.

### 🅐 GitHub Pages (BEPUL, ENG OSON)

1. **github.com** ga kiring (ro'yxatdan o'ting)
2. `New repository` bosing
3. Nom bering: `xonhalol-shop`
4. **Public** qiling
5. `Create repository` bosing
6. `Add file → Upload files` bosing
7. `xonhalol_final.html` ni yuklang
8. `Commit changes` bosing
9. `Settings → Pages → Branch: main → Save`
10. URL tayyor:
    ```
    https://SIZNING_USERNAME.github.io/xonhalol-shop/xonhalol_final.html
    ```

### 🅑 Vercel (BEPUL, TEZROQ)

1. **vercel.com** ga kiring
2. `Add New → Project`
3. Faylni yuklang
4. Deploy bosing
5. URL olasiz: `https://xonhalol-shop.vercel.app`

---

## 4️⃣ MINI APP URL NI BOTGA QO'SHISH

URL ni `xonhalol_bot.py` dagi:
```python
MINI_APP_URL = "https://SIZNING_USERNAME.github.io/xonhalol-shop/xonhalol_final.html"
```
ga qo'ying.

---

## 5️⃣ BOTGA MENU TUGMA QO'SHISH (@BotFather)

1. @BotFather ga yozing
2. `/mybots` → Botingizni tanlang
3. `Bot Settings → Menu Button`
4. `Configure menu button`
5. URL kiriting: Mini App URL ingiz
6. Matn kiriting: `🛍 Do'konni ochish`

---

## 6️⃣ BOTNI SERVERDA ISHLATISH

### Kompyuteringizda (test uchun):
```bash
# 1. Python kutubxonasini o'rnating
pip install python-telegram-bot==20.7

# 2. Botni ishga tushiring
python xonhalol_bot.py
```

### Doimiy ishlashi uchun (VPS server):

**Railway.app** (BEPUL, ENG OSON):
1. **railway.app** ga kiring
2. `New Project → Deploy from GitHub`
3. `xonhalol_bot.py` va `requirements.txt` ni yuklang
4. Environment Variables ga:
   - `BOT_TOKEN` = tokeningiz
   - `ADMIN_ID` = ID ingiz
   - `MINI_APP_URL` = URL ingiz
5. Deploy bosing → Bot 24/7 ishlaydi!

---

## 7️⃣ BOT ISHLASH TARTIBI

```
Foydalanuvchi /start bosadi
        ↓
Til tanlaydi (UZ/RU)
        ↓
Asosiy menyu ko'rinadi
        ↓
🛍 Mahsulotlar → Mini App ochiladi
        ↓
Savatga qo'shib "Buyurtma berish" bosadi
        ↓
Bot so'raydi: Ism → Telefon → Manzil → To'lov
        ↓
Buyurtma tasdiqlanadi
        ↓
Adminga (sizga) xabar keladi
        ↓
Siz: Qabul / Yuborildi / Yetkazildi bosasiz
        ↓
Foydalanuvchiga status xabari ketadi
```

---

## ✅ TEKSHIRISH RO'YXATI

- [ ] `BOT_TOKEN` to'ldirilgan
- [ ] `ADMIN_ID` to'ldirilgan
- [ ] `xonhalol_final.html` internet ga yuklangan (HTTPS)
- [ ] `MINI_APP_URL` to'ldirilgan
- [ ] `pip install python-telegram-bot==20.7` qilingan
- [ ] Bot ishga tushirilgan
- [ ] @BotFather da Menu Button sozlangan
- [ ] `/start` bosildi va ishladi ✅

---

## ❓ KO'P SO'RALADIGAN SAVOLLAR

**Q: Mini App ochilmayapti?**
A: URL HTTPS bo'lishi shart. `http://` ishlamaydi.

**Q: Admin xabari kelmayapti?**
A: `ADMIN_ID` to'g'ri kiritilganini tekshiring (int, string emas).

**Q: Bot to'xtab qolayapti?**
A: Railway yoki VPS da ishlatish kerak. Kompyuter o'chsa bot ham to'xtaydi.

**Q: Narxlarni o'zgartirmoqchiman?**
A: `xonhalol_final.html` faylini oching, `price:` qiymatlarini o'zgartiring, qaytadan yuklang.
