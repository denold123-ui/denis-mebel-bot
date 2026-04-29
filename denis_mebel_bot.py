import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8624049476:AAFKaCgfpW7-l34LPpqRkfQRBEkN_dqGjOQ"  # Токен от BotFather
ADMIN_CHAT_ID = "1084100048"  # Твой Telegram ID (узнай у @userinfobot)

# ===== ЭТАПЫ СБОРА ЗАЯВКИ =====
ASK_NAME, ASK_DETAILS, ASK_CITY, ASK_CONTACT = range(4)

logging.basicConfig(level=logging.INFO)

# ===== ГЛАВНОЕ МЕНЮ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖥 Проектирование", callback_data="proekt")],
        [InlineKeyboardButton("🔧 Установка и сборка", callback_data="ustanovka")],
        [InlineKeyboardButton("🛋 Мебель на заказ", callback_data="zakaz")],
        [InlineKeyboardButton("📁 Мои работы", callback_data="portfolio")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "Привет! 👋 Меня зовут Денис, занимаюсь мебелью уже 6 лет.\n\n"
        "Помогу вам с:\n"
        "🖥 Проектированием мебели в программе Базис Мебельщик\n"
        "🔧 Установкой и сборкой мебели (Уфа)\n"
        "🛋 Мебелью на заказ под ваши размеры и пожелания\n\n"
        "Что вас интересует?"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

# ===== ОБРАБОТКА КНОПОК МЕНЮ =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "proekt":
        keyboard = [
            [InlineKeyboardButton("🍳 Кухня", callback_data="cat_кухню"),
             InlineKeyboardButton("🚪 Шкаф", callback_data="cat_шкаф")],
            [InlineKeyboardButton("👗 Гардеробная", callback_data="cat_гардеробную"),
             InlineKeyboardButton("🏠 Прихожая", callback_data="cat_прихожую")],
            [InlineKeyboardButton("🧸 Детская", callback_data="cat_детскую мебель"),
             InlineKeyboardButton("📦 Другое", callback_data="cat_другое")],
            [InlineKeyboardButton("◀️ Назад", callback_data="back")],
        ]
        await query.edit_message_text(
            "🖥 *Проектирование в Базис Мебельщик*\n\n"
            "Делаю точные проекты удалённо по всей России 🇷🇺\n\n"
            "Вы получите:\n"
            "✅ 3D-модель вашей мебели\n"
            "✅ Чертежи всех деталей с размерами\n"
            "✅ Карту раскроя для экономии материала\n"
            "✅ Полный список фурнитуры\n\n"
            "💰 Стоимость от 2 500 руб, срок 1-2 дня\n\n"
            "Какую мебель хотите спроектировать?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        context.user_data["service"] = "Проектирование"

    elif data == "ustanovka":
        keyboard = [
            [InlineKeyboardButton("🍳 Кухня", callback_data="cat_кухню"),
             InlineKeyboardButton("🚪 Шкаф", callback_data="cat_шкаф")],
            [InlineKeyboardButton("👗 Гардеробная", callback_data="cat_гардеробную"),
             InlineKeyboardButton("🏠 Прихожая", callback_data="cat_прихожую")],
            [InlineKeyboardButton("🧸 Детская", callback_data="cat_детскую мебель"),
             InlineKeyboardButton("📦 Другое", callback_data="cat_другое")],
            [InlineKeyboardButton("◀️ Назад", callback_data="back")],
        ]
        await query.edit_message_text(
            "🔧 *Установка и сборка мебели*\n\n"
            "Работаю в Уфе и Башкортостане 📍\n\n"
            "✅ Опыт сборки 6 лет\n"
            "✅ Работаю аккуратно, без царапин\n"
            "✅ Мебель любой сложности\n\n"
            "Что нужно собрать?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        context.user_data["service"] = "Установка и сборка"

    elif data == "zakaz":
        keyboard = [
            [InlineKeyboardButton("🍳 Кухня", callback_data="cat_кухню"),
             InlineKeyboardButton("🚪 Шкаф", callback_data="cat_шкаф")],
            [InlineKeyboardButton("👗 Гардеробная", callback_data="cat_гардеробную"),
             InlineKeyboardButton("🏠 Прихожая", callback_data="cat_прихожую")],
            [InlineKeyboardButton("🧸 Детская", callback_data="cat_детскую мебель"),
             InlineKeyboardButton("📦 Другое", callback_data="cat_другое")],
            [InlineKeyboardButton("◀️ Назад", callback_data="back")],
        ]
        await query.edit_message_text(
            "🛋 *Мебель на заказ*\n\n"
            "Изготавливаю корпусную мебель точно под ваши размеры и интерьер\n\n"
            "✅ Работаю в Уфе и по всей России\n"
            "✅ Любые размеры и конфигурации\n"
            "✅ Качественные материалы\n\n"
            "Что хотите сделать?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        context.user_data["service"] = "Мебель на заказ"

    elif data == "portfolio":
        keyboard = [
            [InlineKeyboardButton("🍳 Кухни", callback_data="port_кухни"),
             InlineKeyboardButton("🚪 Шкафы", callback_data="port_шкафы")],
            [InlineKeyboardButton("👗 Гардеробные", callback_data="port_гардеробные"),
             InlineKeyboardButton("🏠 Прихожие", callback_data="port_прихожие")],
            [InlineKeyboardButton("🧸 Детские", callback_data="port_детские")],
            [InlineKeyboardButton("◀️ Назад", callback_data="back")],
        ]
        await query.edit_message_text(
            "📁 *Мои работы*\n\nВыберите категорию:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("port_"):
        cat = data.replace("port_", "")
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="portfolio")]]
        await query.edit_message_text(
            f"📸 Фото раздела *{cat}* скоро появятся здесь!\n\n"
            f"Пока можете посмотреть все работы на Авито или написать мне напрямую.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "back":
        await start(update, context)

    elif data.startswith("cat_"):
        cat = data.replace("cat_", "")
        context.user_data["category"] = cat
        keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data="back")]]
        await query.edit_message_text(
            f"Отлично! Оформляем заявку на *{cat}*\n\n"
            f"Как вас зовут?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return ASK_NAME

    return ConversationHandler.END

# ===== СБОР ЗАЯВКИ =====
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        f"Приятно познакомиться, {update.message.text}! 😊\n\n"
        f"Опишите что хотите сделать — размеры, пожелания, можете прислать фото или эскиз 📐"
    )
    return ASK_DETAILS

async def ask_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text
    await update.message.reply_text("Из какого вы города? 📍")
    return ASK_CITY

async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text(
        "Последний вопрос — ваш номер телефона или Telegram для связи? 📱"
    )
    return ASK_CONTACT

async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text

    # Подтверждение клиенту
    keyboard = [[InlineKeyboardButton("🏠 В главное меню", callback_data="back")]]
    await update.message.reply_text(
        "✅ Заявка принята!\n\n"
        "Денис свяжется с вами в течение часа.\n\n"
        "Если срочно — напишите напрямую: @Denis_Mebel",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # Уведомление тебе
    d = context.user_data
    notification = (
        f"🔔 НОВАЯ ЗАЯВКА!\n\n"
        f"👤 Имя: {d.get('name', '—')}\n"
        f"🛠 Услуга: {d.get('service', '—')}\n"
        f"🪑 Категория: {d.get('category', '—')}\n"
        f"📝 Описание: {d.get('details', '—')}\n"
        f"📍 Город: {d.get('city', '—')}\n"
        f"📱 Контакт: {d.get('contact', '—')}\n"
        f"💬 Telegram: @{update.effective_user.username or 'нет username'}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=notification)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    return ConversationHandler.END

# ===== ЗАПУСК БОТА =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_details)],
            ASK_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)],
            ASK_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contact)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern="back")],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
