from core.storage import add_habit, list_habits, habit_done, set_goal
from core.storage import get_lang, get_uid
from core.texts import t
from handlers.common import kb_habits, kb_main

async def habits_handler(update, context):
    user = update.effective_user
    msg = update.message.text
    lang = get_lang(user.id)
    uid = get_uid(user.id)
    ud = context.user_data

    if msg == t(lang, "btn_add"):
        ud["habits_mode"] = "add_name"
        await update.message.reply_text(t(lang, "addhabit_prompt"), reply_markup=kb_habits(lang))
        return

    if ud.get("habits_mode") == "add_name":
        add_habit(uid, msg)
        ud["habits_mode"] = None
        await update.message.reply_text(t(lang, "habit_added", name=msg), reply_markup=kb_habits(lang))
        return

    if msg == t(lang, "btn_list"):
        habits = list_habits(uid)
        if not habits:
            await update.message.reply_text(t(lang, "done_no_habits"), reply_markup=kb_habits(lang))
            return
        txt = t(lang, "list_header") + "\n"
        for hid, name, streak, goal in habits:
            txt += t(lang, "list_line", id=hid, name=name, streak=streak) + "\n"
        await update.message.reply_text(txt, reply_markup=kb_habits(lang))
        return

    if msg == t(lang, "btn_done"):
        habits = list_habits(uid)
        if not habits:
            await update.message.reply_text(t(lang, "done_no_habits"), reply_markup=kb_habits(lang))
            return
        ud["habits_mode"] = "choose_done"
        txt = t(lang, "done_select") + "\n"
        for hid, name, streak, goal in habits:
            txt += f"{hid}. {name}\n"
        await update.message.reply_text(txt, reply_markup=kb_habits(lang))
        return

    if ud.get("habits_mode") == "choose_done" and msg.isdigit():
        habit_done(int(msg))
        ud["habits_mode"] = None
        await update.message.reply_text(t(lang, "done_success"), reply_markup=kb_habits(lang))
        return

    if msg == t(lang, "btn_goal"):
        habits = list_habits(uid)
        ud["habits_mode"] = "choose_goal"
        txt = t(lang, "goal_select") + "\n"
        for hid, name, streak, goal in habits:
            txt += f"{hid}. {name}\n"
        await update.message.reply_text(txt, reply_markup=kb_habits(lang))
        return

    if ud.get("habits_mode") == "choose_goal" and msg.isdigit():
        ud["goal_habit_id"] = int(msg)
        ud["habits_mode"] = "goal_value"
        await update.message.reply_text(t(lang, "goal_enter"), reply_markup=kb_habits(lang))
        return

    if ud.get("habits_mode") == "goal_value":
        set_goal(ud["goal_habit_id"], int(msg))
        ud["habits_mode"] = None
        await update.message.reply_text(t(lang, "goal_saved"), reply_markup=kb_habits(lang))
        return

    if msg == t(lang, "btn_stats"):
        habits = list_habits(uid)
        txt = t(lang, "habitstats_header") + "\n"
        for hid, name, streak, goal in habits:
            txt += t(lang, "habitstats_line", name=name, streak=streak, goal=goal) + "\n"
        await update.message.reply_text(txt, reply_markup=kb_habits(lang))
        return
