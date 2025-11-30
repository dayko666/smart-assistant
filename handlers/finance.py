from core.storage import add_fin, finance_stats
from core.storage import get_lang, get_uid
from core.texts import t
from handlers.common import kb_finance

async def finance_handler(update, context):
    user = update.effective_user
    msg = update.message.text
    lang = get_lang(user.id)
    uid = get_uid(user.id)
    ud = context.user_data

    if msg == t(lang, "btn_expense"):
        ud["fin_mode"] = "amount_exp"
        await update.message.reply_text(t(lang, "fin_amount"), reply_markup=kb_finance(lang))
        return

    if msg == t(lang, "btn_income"):
        ud["fin_mode"] = "amount_inc"
        await update.message.reply_text(t(lang, "fin_amount"), reply_markup=kb_finance(lang))
        return

    if ud.get("fin_mode") in ("amount_exp", "amount_inc"):
        ud["fin_amount"] = float(msg.replace(",", "."))
        ud["fin_type"] = "expense" if ud["fin_mode"] == "amount_exp" else "income"
        ud["fin_mode"] = "category"
        await update.message.reply_text(t(lang, "fin_category"), reply_markup=kb_finance(lang))
        return

    if ud.get("fin_mode") == "category":
        ud["fin_category"] = msg
        ud["fin_mode"] = "note"
        await update.message.reply_text(t(lang, "fin_note"), reply_markup=kb_finance(lang))
        return

    if ud.get("fin_mode") == "note":
        note = None if msg == "-" else msg
        add_fin(uid, ud["fin_type"], ud["fin_amount"], ud["fin_category"], note)
        ok = "expense_added" if ud["fin_type"] == "expense" else "income_added"
        ud["fin_mode"] = None
        await update.message.reply_text(t(lang, ok), reply_markup=kb_finance(lang))
        return

    if msg == t(lang, "btn_stats"):
        income, expense, bycat = finance_stats(uid)
        bal = income - expense
        txt = t(lang, "fin_stats_header") + "\n"
        txt += t(lang, "fin_balance", income=income, expense=expense, balance=bal) + "\n"
        for cat, amount in bycat:
            txt += t(lang, "fin_stats_line", category=cat, amount=amount) + "\n"
        await update.message.reply_text(txt, reply_markup=kb_finance(lang))
        return
