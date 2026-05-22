import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PDF_URL = "https://example.com/style-guide.pdf"

QUESTIONS = [
    {
        "text": "Вопрос 1 из 10 👗\n\nПредставь, что ты открываешь шкаф утром в обычный день.\nКакой силуэт одежды ты тянешься надеть в первую очередь?",
        "options": [
            ("👔 Чёткий, приталенный, строгий", "klassika"),
            ("🌸 Мягкий, женственный, с деталями", "romantika"),
            ("🌿 Свободный, удобный, без лишнего", "casual"),
        ],
    },
    {
        "text": "Вопрос 2 из 10 👠\n\nКакая обувь чаще всего на твоих ногах?",
        "options": [
            ("👠 Каблук или лодочки", "klassika"),
            ("🌸 Балетки или мюли", "romantika"),
            ("👟 Кеды или лоферы", "casual"),
        ],
    },
    {
        "text": "Вопрос 3 из 10 🎨\n\nКакие цвета преобладают в твоём гардеробе?",
        "options": [
            ("🖤 Чёрный, белый, бежевый, серый", "klassika"),
            ("🌸 Пудровый, розовый, лавандовый", "romantika"),
            ("🌿 Джинсовый, хаки, терракота", "casual"),
        ],
    },
    {
        "text": "Вопрос 4 из 10 👜\n\nКакую сумку ты чаще выбираешь?",
        "options": [
            ("💼 Структурированная классическая сумка", "klassika"),
            ("👛 Маленькая сумочка-клатч или мини", "romantika"),
            ("🎒 Тоут, шоппер или рюкзак", "casual"),
        ],
    },
    {
        "text": "Вопрос 5 из 10 💄\n\nКакой макияж тебе ближе всего?",
        "options": [
            ("✨ Чёткий, сдержанный, стрелки или нюд", "klassika"),
            ("🌸 Нежный, с румянами и блеском", "romantika"),
            ("🌿 Минимальный или вообще без макияжа", "casual"),
        ],
    },
    {
        "text": "Вопрос 6 из 10 🌟\n\nКак ты относишься к украшениям?",
        "options": [
            ("💎 Классика — жемчуг, золото, минимализм", "klassika"),
            ("🌸 Обожаю! Серьги, кольца, слои", "romantika"),
            ("🌿 Редко ношу или только одно украшение", "casual"),
        ],
    },
    {
        "text": "Вопрос 7 из 10 🛍️\n\nКак ты выбираешь одежду в магазине?",
        "options": [
            ("👔 Ищу качественные базовые вещи", "klassika"),
            ("🌸 Привлекают детали — кружево, принты, рюши", "romantika"),
            ("🌿 Главное — удобно и можно носить каждый день", "casual"),
        ],
    },
    {
        "text": "Вопрос 8 из 10 🌍\n\nКуда ты идёшь — как одеваешься?",
        "options": [
            ("👔 Всегда выгляжу собранно и аккуратно", "klassika"),
            ("🌸 Стараюсь выглядеть женственно даже в будни", "romantika"),
            ("🌿 Удобно и стильно — это моё правило", "casual"),
        ],
    },
    {
        "text": "Вопрос 9 из 10 💭\n\nКакой образ тебя вдохновляет больше всего?",
        "options": [
            ("👑 Элегантная бизнес-леди или француженка", "klassika"),
            ("🌸 Нежная героиня романтического фильма", "romantika"),
            ("🌿 Стильная девушка с улицы Нью-Йорка", "casual"),
        ],
    },
    {
        "text": "Вопрос 10 из 10 🌟\n\nПоследний 🌸\n\nЧто чаще всего говорят о твоём стиле подруги или близкие?",
        "options": [
            ("✨ «Ты всегда так элегантно выглядишь»", "klassika"),
            ("🌸 «Ты такая женственная и нежная»", "romantika"),
            ("🌿 «Ты всегда выглядишь естественно и круто»", "casual"),
        ],
    },
]


def make_score_bar(score: int, total: int = 10) -> str:
    filled = round((score / total) * 10) if total else 0
    empty = 10 - filled
    return "█" * filled + "░" * empty


def get_result_text(scores: dict) -> str:
    klassika = scores.get("klassika", 0)
    romantika = scores.get("romantika", 0)
    casual = scores.get("casual", 0)
    total = klassika + romantika + casual or 1

    bar_k = make_score_bar(klassika, total)
    bar_r = make_score_bar(romantika, total)
    bar_c = make_score_bar(casual, total)

    winner = max(scores, key=scores.get) if scores else "casual"

    if winner == "klassika":
        return (
            "Готово! Твой результат: 👑\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "СТИЛЬ — КЛАССИКА\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ты — женщина с безупречным вкусом.\n"
            "Твой стиль говорит об уверенности,\n"
            "статусе и уважении к себе.\n"
            "Ты выбираешь качество, а не количество.\n\n"
            "✅ ТВОИ БАЗОВЫЕ ВЕЩИ:\n"
            "• Белая рубашка\n"
            "• Прямые брюки\n"
            "• Приталенный пиджак\n"
            "• Платье-футляр\n"
            "• Тренч бежевый или чёрный\n"
            "• Юбка-карандаш\n"
            "• Лодочки на каблуке\n"
            "• Структурированная сумка\n\n"
            "✅ ТВОИ ЦВЕТА:\n"
            "• Чёрный и белый\n"
            "• Бежевый и кремовый\n"
            "• Серый всех оттенков\n"
            "• Тёмно-синий (navy)\n"
            "• Бордо и тёмно-зелёный\n\n"
            "💡 ТВОЙ ПРИНЦИП:\n"
            "Лучше меньше, но лучше.\n"
            "Каждая вещь — инвестиция.\n\n"
            "⚠️ ЧАСТАЯ ОШИБКА:\n"
            "Слишком строгий образ без живых деталей —\n"
            "добавь один яркий акцент.\n\n"
            "📊 Твои баллы:\n"
            f"👑 Классика:  {bar_k}\n"
            f"🌸 Романтика: {bar_r}\n"
            f"🌿 Casual:    {bar_c}"
        )
    elif winner == "romantika":
        return (
            "Готово! Твой результат: 🌸\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "СТИЛЬ — РОМАНТИКА\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ты — женщина с тонким чувством\n"
            "красоты и женственности.\n"
            "Твой стиль притягивает взгляды\n"
            "и создаёт особую атмосферу вокруг тебя.\n\n"
            "✅ ТВОИ БАЗОВЫЕ ВЕЩИ:\n"
            "• Платье с цветочным принтом\n"
            "• Блузка с рюшами или кружевом\n"
            "• Юбка миди с воланом\n"
            "• Кардиган нежного цвета\n"
            "• Балетки или мюли\n"
            "• Изящные украшения\n"
            "• Сумочка-клатч или мини-сумка\n\n"
            "✅ ТВОИ ЦВЕТА:\n"
            "• Пудровый и нежно-розовый\n"
            "• Лавандовый и сиреневый\n"
            "• Молочный и кремовый\n"
            "• Персиковый и мятный\n"
            "• Нежно-голубой\n\n"
            "💡 ТВОЙ ПРИНЦИП:\n"
            "Детали решают всё.\n"
            "Один красивый элемент меняет весь образ.\n\n"
            "⚠️ ЧАСТАЯ ОШИБКА:\n"
            "Слишком много деталей сразу —\n"
            "выбери один акцент: либо украшения,\n"
            "либо принт, либо фактура.\n\n"
            "📊 Твои баллы:\n"
            f"👑 Классика:  {bar_k}\n"
            f"🌸 Романтика: {bar_r}\n"
            f"🌿 Casual:    {bar_c}"
        )
    else:
        return (
            "Готово! Твой результат: 🌿\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "СТИЛЬ — CASUAL\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ты — женщина, которая ценит\n"
            "свободу и комфорт без потери стиля.\n"
            "Твой образ всегда выглядит\n"
            "естественно и современно.\n\n"
            "✅ ТВОИ БАЗОВЫЕ ВЕЩИ:\n"
            "• Прямые джинсы\n"
            "• Белая футболка и базовые топы\n"
            "• Оверсайз рубашка\n"
            "• Трикотажный свитер\n"
            "• Кеды или лоферы\n"
            "• Тоут или рюкзак\n"
            "• Джинсовая куртка или бомбер\n\n"
            "✅ ТВОИ ЦВЕТА:\n"
            "• Белый и светло-серый\n"
            "• Джинсовый синий\n"
            "• Хаки и оливковый\n"
            "• Терракота и кирпичный\n"
            "• Молочный и бежевый\n\n"
            "💡 ТВОЙ ПРИНЦИП:\n"
            "Комфорт — это не значит скучно.\n"
            "Один стильный акцент делает образ запоминающимся.\n\n"
            "⚠️ ЧАСТАЯ ОШИБКА:\n"
            "Слишком много оверсайз вещей в одном образе —\n"
            "один свободный элемент, второй — по фигуре.\n\n"
            "📊 Твои баллы:\n"
            f"👑 Классика:  {bar_k}\n"
            f"🌸 Романтика: {bar_r}\n"
            f"🌿 Casual:    {bar_c}"
        )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👗 Да, хочу узнать свой стиль!", callback_data="start_test")],
        [InlineKeyboardButton("📥 Сначала получить PDF бесплатно", callback_data="get_pdf")],
        [InlineKeyboardButton("💬 Написать Марте напрямую", callback_data="contact")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    text = (
        "Привет! 👋\n"
        "Я — бот стилиста Marta Franz 🌸\n\n"
        "За 2 минуты помогу тебе понять\n"
        "свой настоящий стиль — тот, который отражает тебя\n"
        "и в котором ты чувствуешь себя собой.\n\n"
        "Готова?"
    )
    await update.message.reply_text(text, reply_markup=main_menu_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        context.user_data.clear()
        text = (
            "Привет! 👋\n"
            "Я — бот стилиста Marta Franz 🌸\n\n"
            "За 2 минуты помогу тебе понять\n"
            "свой настоящий стиль — тот, который отражает тебя\n"
            "и в котором ты чувствуешь себя собой.\n\n"
            "Готова?"
        )
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())

    elif data == "get_pdf":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Скачать PDF", url=PDF_URL)],
            [InlineKeyboardButton("👗 Пройти тест прямо сейчас", callback_data="start_test")],
        ])
        await query.edit_message_text(
            "Держи! 🎁\n\n"
            "Это PDF с подробным описанием 3 основных стилей.\n"
            "⬇️ Скачай и возвращайся — пройдём тест вместе:",
            reply_markup=keyboard,
        )

    elif data == "contact":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 Написать в Telegram", url="https://t.me/La_Perla_21")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
        ])
        await query.edit_message_text(
            "Marta Franz на связи 🌸\n\n"
            "Выбери удобный способ:\n"
            "📞 Позвонить: +7-999-03-03-014\n"
            "✉️ Email: todes-07@mail.ru\n"
            "📱 Telegram: @La_Perla_21",
            reply_markup=keyboard,
        )

    elif data == "start_test":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Начать тест", callback_data="begin_test")],
        ])
        await query.edit_message_text(
            "Отлично, начнём! ✨\n\n"
            "Тест состоит из 10 вопросов.\n"
            "Выбирай первое, что приходит в голову — не думай долго.\n"
            "Нет правильных или неправильных ответов. Только твой стиль 🌸\n\n"
            "Поехали!",
            reply_markup=keyboard,
        )

    elif data == "begin_test":
        context.user_data["scores"] = {"klassika": 0, "romantika": 0, "casual": 0}
        context.user_data["question"] = 0
        await send_question(query, context)

    elif data.startswith("answer_"):
        _, style = data.split("_", 1)
        scores = context.user_data.get("scores", {"klassika": 0, "romantika": 0, "casual": 0})
        scores[style] = scores.get(style, 0) + 1
        context.user_data["scores"] = scores

        q_index = context.user_data.get("question", 0) + 1
        context.user_data["question"] = q_index

        if q_index < len(QUESTIONS):
            await send_question(query, context)
        else:
            await show_result(query, context)

    elif data == "book_session":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 Написать в Telegram", url="https://t.me/La_Perla_21")],
            [InlineKeyboardButton("📞 Позвонить: +7-999-03-03-014", callback_data="show_phone")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
        ])
        await query.edit_message_text(
            "Marta Franz готова помочь! 🌸\n\n"
            "Форматы работы:\n\n"
            "💼 Разбор гардероба — разберём что есть, что докупить\n"
            "и как сочетать (от 1000 руб.)\n\n"
            "👗 Экспресс-разбор образа — пришли фото,\n"
            "получи детальный разбор (от 700 руб.)\n\n"
            "🎨 Полный стилистический разбор\n"
            "Индивидуально — цветотип,\n"
            "стиль, гардероб, шопинг-лист\n\n"
            "Напиши Марте напрямую 👇",
            reply_markup=keyboard,
        )

    elif data == "show_phone":
        await query.answer("📞 +7-999-03-03-014", show_alert=True)

    elif data == "restart_test":
        context.user_data.clear()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Начать тест", callback_data="begin_test")],
        ])
        await query.edit_message_text(
            "Отлично, начнём! ✨\n\n"
            "Тест состоит из 10 вопросов.\n"
            "Выбирай первое, что приходит в голову — не думай долго.\n"
            "Нет правильных или неправильных ответов. Только твой стиль 🌸\n\n"
            "Поехали!",
            reply_markup=keyboard,
        )

    else:
        await query.answer("Я не понимаю эту команду.", show_alert=True)


async def send_question(query, context: ContextTypes.DEFAULT_TYPE):
    q_index = context.user_data.get("question", 0)
    question = QUESTIONS[q_index]
    buttons = [
        [InlineKeyboardButton(label, callback_data=f"answer_{style}")]
        for label, style in question["options"]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(question["text"], reply_markup=keyboard)


async def show_result(query, context: ContextTypes.DEFAULT_TYPE):
    scores = context.user_data.get("scores", {})
    await query.edit_message_text("Секунду... ⏳\n\nСчитаю твои результаты 🌸")

    result_text = get_result_text(scores)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Записаться на разбор", callback_data="book_session")],
        [InlineKeyboardButton("🔄 Пройти тест заново", callback_data="restart_test")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])
    await query.edit_message_text(result_text, reply_markup=keyboard)


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан! Добавь его в переменные окружения.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
