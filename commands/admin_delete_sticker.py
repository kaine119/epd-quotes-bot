from telegram import Update, constants, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters

STICKER_TO_DELETE = range(1)

admin_id = 0

def set_admin_id(uid):
    global admin_id
    admin_id = uid

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message.from_user.id != admin_id):
        await update.message.reply_text("Admin-only command. Sorry!")
        return
    await update.message.reply_text("Please send the sticker to delete.")
    return STICKER_TO_DELETE
    
async def sticker_to_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message.from_user.id != admin_id):
        await update.message.reply_text("Admin-only command. Sorry!")
        return
    await context.bot.delete_sticker_from_set(update.message.sticker.file_id)
    await update.message.reply_text("Done")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Cancelled.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

handler = ConversationHandler(
    entry_points=[CommandHandler("admin_delete_sticker", start)],
    states={
        STICKER_TO_DELETE: [MessageHandler(filters.Sticker.STATIC, sticker_to_delete)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)