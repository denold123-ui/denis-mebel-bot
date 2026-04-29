import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8624049476:AAFKaCgfpW7-l34LPpqRkfQRBEkN_dqGjOQ"
ADMIN_CHAT_ID = "1084100048"

ASK_NAME, ASK_DETAILS, ASK_CITY, ASK_CONTACT = range(4)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖥 Проектирование", callback_data="proekt")],
        [InlineKeyboardButton("🔧 Установка и сборка", callback_data="ustanovka")],
        [InlineKeyboardButton("🛋 Мебель на заказ", callback_data="zakaz")],
        [InlineKeyboardButton("📁 Мои работы", callback_data="portfolio")],
    ]
    text = (
        "Привет! 👋 Меня зовут Денис, занимаюсь мебелью уже 6 лет.\n\n"
        "Помогу вам с:\n"
        "🖥 Проектированием мебели в программе Базис Мебельщик\n"
        "🔧 Установкой и сборкой мебели (Уфа)\n"
        "🛋 Мебелью на заказ под ваши размеры и пожелания\n\n"
        "Что вас интересует?"
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

def get_category_keyboard(back_target):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍳 Кухня", callback_data="cat_кухню"),
         InlineKeyboardButton("🚪 Шкаф", callback_data="cat_шкаф")],
        [InlineKeyboardButton("👗 Гардеробная", callback_data="cat_гардеробную"),
         InlineKeyboardButton("🏠 Прихожая", callback_data="cat_прихожую")],
        [InlineKeyboardButton("🧸 Детская", callback_data="cat_детскую"),
         InlineKeyboardButton("📦 Другое", callback_data="cat_другое")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await start(update, context)
        return ConversationHandler.END

    elif data == "proekt":
        context.user_data["service"] = "Проектирование"
        await query.edit_message_text(
            "🖥 Проектирование в Базис Мебельщик\n\n"
            "Делаю точные проекты удалённо по всей России 🇷🇺\n\n"
            "✅ 3D-модель\n✅ Чертежи с размерами\n✅ Карта раскроя\n✅ Список фурнитуры\n\n"
            "💰 От 2 500 руб, срок 1-2 дня\n\nКакую мебель хотите спроектировать?",
            reply_markup=get_category_keyboard("back")
        )

    elif data == "ustanovka":
        context.user_data["service"] = "Установка и сборка"
        await query.edit_message_text(
            "🔧 Установка и сборка мебели\n\nРаботаю в Уфе 📍\n\n"
            "✅ Опыт 6 лет\n✅ Аккуратно, без царапин\n✅ Мебель любой сложности\n\nЧто нужно собрать?",
            reply_markup=get_category_keyboard("back")
        )

    elif data == "zakaz":
        context.user_data["service"] = "Мебель на заказ"
        await query.edit_message_text(
            "🛋 Мебель на заказ\n\nТочно под ваши размеры и интерьер\n\n"
            "✅ Уфа и вся Россия\n✅ Любые размеры\n✅ Качественные материалы\n\nЧто хотите сделать?",
            reply_markup=get_category_keyboard("back")
        )

    elif data == "portfolio":
        await query.edit_message_text(
            "📁 Мои работы\n\nВыберите категорию:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🍳 Кухни", callback_data="port_кухни"),
                 InlineKeyboardButton("🚪 Шкафы", callback_data="port_шкафы")],
                [InlineKeyboardButton("👗 Гардеробные", callback_data="port_гардеробные"),
                 InlineKeyboardButton("🏠 Прихожие", callback_data="port_прихожие")],
                [InlineKeyboardButton("🧸 Детские", callback_data="port_детские")],
                [InlineKeyboardButton("◀️ Назад", callback_data="back")],
            ])
        )

    elif data.startswith("port_"):
        cat = data.replace("port_", "")
        await query.edit_message_text(
            f"📸 Раздел '{cat}' — фото скоро появятся!\n\nПока напишите мне напрямую для просмотра портфолио.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data="portfolio")]])
        )

    elif data.startswith("cat_"):
        cat = data.replace("cat_", "")
        context.user_data["category"] = cat
        await query.edit_message_text(
            f"Оформляем заявку на {cat}\n\nКак вас зовут?",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Отмена", callback_data="back")]])
        )
        return ASK_NAME

    return ConversationHandler.END

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        f"Приятно познакомиться, {update.message.text}! 😊\n\n"
        "Опишите что хотите сделать — размеры, пожелания, можно прислать фото или эскиз 📐"
    )
    return ASK_DETAILS

async def ask_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text
    await update.message.reply_text("Из какого вы города? 📍")
    return ASK_CITY

async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Ваш номер телефона или Telegram для связи? 📱")
    return ASK_CONTACT

async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text(
        "✅ Заявка принята!\n\nДенис свяжется с вами в течение часа.\n\nЕсли срочно — напишите напрямую: @Denis_Mebel",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 В главное меню", callback_data="back")]])
    )
    d = context.user_data
    notification = (
        f"🔔 НОВАЯ ЗАЯВКА!\n\n"
        f"👤 Имя: {d.get('name','—')}\n"
        f"🛠 Услуга: {d.get('service','—')}\n"
        f"🪑 Категория: {d.get('category','—')}\n"
        f"📝 Описание: {d.get('details','—')}\n"
        f"📍 Город: {d.get('city','—')}\n"
        f"📱 Контакт: {d.get('contact','—')}\n"
        f"💬 TG: @{update.effective_user.username or 'нет'}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=notification)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
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
    app.add_handler(conv)
    print("✅ Бот запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
