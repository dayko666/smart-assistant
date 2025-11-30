from telegram import ReplyKeyboardMarkup
from core.storage import get_user, create_user, get_lang, set_lang
from core.texts import t

def kb_main(lang):
    return ReplyKeyboardMarkup(
        [
            [t(lang, "btn_habits"), t(lang, "btn_tasks")],
            [t(lang, "btn_finance")]
        ],
        resize_keyboard=True
    )

def kb_habits(lang):
    return ReplyKeyboardMarkup(
        [
            [t(lang, "btn_add"), t(lang, "btn_done")],
            [t(lang, "btn_list"), t(lang, "btn_goal")],
            [t(lang, "btn_stats")],
            [t(lang, "btn_back")]
        ],
        resize_keyboard=True
    )

def kb_tasks(lang):
    return ReplyKeyboardMarkup(
        [
            [t(lang, "btn_add"), t(lang, "btn_list")],
            [t(lang, "btn_done")],
            [t(lang, "btn_back")]
        ],
        resize_keyboard=True
    )

def kb_finance(lang):
    return ReplyKeyboardMarkup(
        [
            [t(lang, "btn_expense"), t(lang, "btn_income")],
            [t(lang, "btn_stats")],
            [t(lang, "btn_back")]
        ],
        resize_keyboard=True
    )

async def start(update, context):
    user = update.effective_user
    tg = user.id
    if not get_user(tg):
        await update.message.reply_text(
            t("en", "language_choose"),
            reply_markup=ReplyKeyboardMarkup([["English", "Русский"]], resize_keyboard=True)
        )
        return
    lang = get_lang(tg)
    context.user_data["section"] = None
    await update.message.reply_text(t(lang, "main_menu"), reply_markup=kb_main(lang))

async def text_router(update, context):
    user = update.effective_user
    msg = update.message.text
    from core.storage import get_lang

    tg = user.id
    lang = get_lang(tg)

    if msg in ["English", "Русский"]:
        lang_new = "en" if msg == "English" else "ru"
        if not get_user(tg):
            create_user(tg, user.full_name, lang_new)
        else:
            set_lang(tg, lang_new)
        context.user_data["section"] = None
        await update.message.reply_text(t(lang_new, "main_menu"), reply_markup=kb_main(lang_new))
        return

    if msg == t(lang, "btn_habits"):
        context.user_data["section"] = "habits"
        await update.message.reply_text(t(lang, "habits_menu"), reply_markup=kb_habits(lang))
        return

    if msg == t(lang, "btn_tasks"):
        context.user_data["section"] = "tasks"
        await update.message.reply_text(t(lang, "tasks_menu"), reply_markup=kb_tasks(lang))
        return

    if msg == t(lang, "btn_finance"):
        context.user_data["section"] = "finance"
        await update.message.reply_text(t(lang, "finance_menu"), reply_markup=kb_finance(lang))
        return

    if msg == t(lang, "btn_back"):
        context.user_data["section"] = None
        await update.message.reply_text(t(lang, "main_menu"), reply_markup=kb_main(lang))
        return

    section = context.user_data.get("section")

    if section == "habits":
        from handlers.habits import habits_handler
        await habits_handler(update, context)
        return

    if section == "tasks":
        from handlers.tasks import tasks_handler
        await tasks_handler(update, context)
        return

    if section == "finance":
        from handlers.finance import finance_handler
        await finance_handler(update, context)
        return
