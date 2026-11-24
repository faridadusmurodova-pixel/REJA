"""
REJA - Telegram Bot kodi (bot/bot.py).
Mavzular: Bot API, Python Telegram Bot, ConversationHandler, PTB botlar.
"""
import os
import sys
import django
from pathlib import Path

# Django muhitini yuklash
ASOSIY_PAPKA = Path(__file__).resolve().parent.parent
sys.path.append(str(ASOSIY_PAPKA))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reja.soz')
django.setup()

from ilova.model import Foydalanuvchi, Vazifa
from django.utils import timezone

try:
    from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
    from telegram.ext import (
        ApplicationBuilder,
        CommandHandler,
        MessageHandler,
        ConversationHandler,
        ContextTypes,
        filters
    )
    PTB_ORRNATILGAN = True
except ImportError:
    PTB_ORRNATILGAN = False

SARLAVHA, MUHIMLIK = range(2)

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '123456789:ABCDEF_NAMUNAVIY_BOT_TOKEN')

async def start_buyrugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """22. Bot API va 25. PTB bot: /start buyrug'i"""
    user_nomi = update.effective_user.first_name
    await update.message.reply_text(
        f"Assalomu alaykum, {user_nomi}!\n"
        "REJA shaxsiy vazifalar botiga xush kelibsiz.\n\n"
        "Buyruqlar:\n"
        "/rejalar - Barcha rejalaringiz\n"
        "/bugun - Bugungi rejalar\n"
        "/yangi - Yangi reja qo'shish (ConversationHandler)\n"
        "/yordam - Yordam"
    )

async def rejalar_buyrugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchining barcha rejalarini ko'rsatish"""
    # Demo uchun birinchi foydalanuvchini olish yoki Telegram ID bo'yicha bog'lash
    user = Foydalanuvchi.objects.first()
    if not user:
        await update.message.reply_text("Bazada foydalanuvchilar topilmadi.")
        return

    vazifalar = Vazifa.objects.filter(foydalanuvchi=user, bajarildi=False)
    if not vazifalar.exists():
        await update.message.reply_text("Sizda hozircha kutilayotgan rejalar yo'q.")
        return

    matn = f"📋 <b>{user.toliq_ism}</b>ning rejalari:\n\n"
    for v in vazifalar:
        matn += f"• <b>{v.sarlavha}</b> ({v.sana})\n"
    await update.message.reply_text(matn, parse_mode='HTML')

async def bugun_buyrugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bugungi rejalarni ko'rsatish"""
    user = Foydalanuvchi.objects.first()
    bugun = timezone.now().date()
    vazifalar = Vazifa.objects.filter(foydalanuvchi=user, sana=bugun)

    if not vazifalar.exists():
        await update.message.reply_text("Bugun uchun rejalar mavjud emas.")
        return

    matn = f"⚡ Bugungi rejalaringiz ({bugun}):\n\n"
    for v in vazifalar:
        holat = "✅" if v.bajarildi else "⏳"
        matn += f"{holat} {v.sarlavha} ({v.vaqt or 'vaqtsiz'})\n"
    await update.message.reply_text(matn)

# 24. CONVERSATIONHANDLER (Muloqot orqali yangi reja qo'shish)
async def yangi_boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muloqotni boshlash"""
    await update.message.reply_text(
        "Yangi reja qo'shish jarayoni boshlandi.\n"
        "Iltimos, rejangiz sarlavhasini yozing:"
    )
    return SARLAVHA

async def sarlavha_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reja sarlavhasini qabul qilish"""
    context.user_data['sarlavha'] = update.message.text
    tugmalar = [['yuqori', 'orta', 'past']]
    await update.message.reply_text(
        "Muhimlik darajasini tanlang:",
        reply_markup=ReplyKeyboardMarkup(tugmalar, one_time_keyboard=True, resize_keyboard=True)
    )
    return MUHIMLIK

async def muhimlik_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muhimlik darajasini qabul qilish va saqlash"""
    muhimlik = update.message.text.lower()
    sarlavha = context.user_data.get('sarlavha')
    user = Foydalanuvchi.objects.first()

    Vazifa.objects.create(
        foydalanuvchi=user,
        sarlavha=sarlavha,
        muhimlik=muhimlik if muhimlik in ['yuqori', 'orta', 'past'] else 'orta',
        sana=timezone.now().date()
    )

    await update.message.reply_text(
        f"✅ Reja muvaffaqiyatli saqlandi:\n"
        f"Nomi: {sarlavha}\nMuhimlik: {muhimlik}",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muloqotni bekor qilish"""
    await update.message.reply_text("Jarayon bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def botni_yaratish():
    """Bot dasturini yig'ish"""
    if not PTB_ORRNATILGAN:
        print("python-telegram-bot o'rnatilmagan.")
        return None

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ConversationHandler qo'shish
    muloqot = ConversationHandler(
        entry_points=[CommandHandler('yangi', yangi_boshlash)],
        states={
            SARLAVHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, sarlavha_qabul)],
            MUHIMLIK: [MessageHandler(filters.TEXT & ~filters.COMMAND, muhimlik_qabul)],
        },
        fallbacks=[CommandHandler('bekor', bekor_qilish)]
    )

    app.add_handler(CommandHandler('start', start_buyrugi))
    app.add_handler(CommandHandler('rejalar', rejalar_buyrugi))
    app.add_handler(CommandHandler('bugun', bugun_buyrugi))
    app.add_handler(muloqot)
    return app

if __name__ == '__main__':
    print("Telegram bot ishga tushirish uchun tayyor.")
    # Ilova ishga tushirish: botni_yaratish().run_polling()
