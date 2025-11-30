from core.storage import add_task, list_tasks, task_done
from core.storage import get_lang, get_uid
from core.texts import t
from handlers.common import kb_tasks

async def tasks_handler(update, context):
    user = update.effective_user
    msg = update.message.text
    lang = get_lang(user.id)
    uid = get_uid(user.id)
    ud = context.user_data

    if msg == t(lang, "btn_add"):
        ud["tasks_mode"] = "title"
        await update.message.reply_text(t(lang, "task_title"), reply_markup=kb_tasks(lang))
        return

    if ud.get("tasks_mode") == "title":
        ud["new_task_title"] = msg
        ud["tasks_mode"] = "due"
        await update.message.reply_text(t(lang, "task_due"), reply_markup=kb_tasks(lang))
        return

    if ud.get("tasks_mode") == "due":
        add_task(uid, ud["new_task_title"], None if msg == "-" else msg)
        ud["tasks_mode"] = None
        await update.message.reply_text(t(lang, "task_added"), reply_markup=kb_tasks(lang))
        return

    if msg == t(lang, "btn_list"):
        tasks = list_tasks(uid)
        txt = t(lang, "task_list_header") + "\n"
        for tid, title, due, done in tasks:
            if done:
                txt += t(lang, "task_done_line", id=tid, title=title) + "\n"
            else:
                txt += t(lang, "task_open", id=tid, title=title, due=due or "-") + "\n"
        await update.message.reply_text(txt, reply_markup=kb_tasks(lang))
        return

    if msg == t(lang, "btn_done"):
        tasks = list_tasks(uid)
        ud["tasks_mode"] = "done_choice"
        txt = t(lang, "task_done_select") + "\n"
        for tid, title, due, done in tasks:
            if not done:
                txt += f"{tid}. {title}\n"
        await update.message.reply_text(txt, reply_markup=kb_tasks(lang))
        return

    if ud.get("tasks_mode") == "done_choice" and msg.isdigit():
        task_done(int(msg))
        ud["tasks_mode"] = None
        await update.message.reply_text(t(lang, "task_done_success"), reply_markup=kb_tasks(lang))
        return
