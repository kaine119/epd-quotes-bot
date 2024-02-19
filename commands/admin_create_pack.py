import telegram
from telegram import Update, constants, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters

admin_id = 0

def set_admin_id(uid):
    global admin_id
    admin_id = uid

async def admin_create_sticker_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message.from_user.id != admin_id):
        await update.message.reply_text("Admin-only command. Sorry!")
        return
    new_sticker = telegram.InputSticker(
        open("./test.png", "rb"),
        ["🧪"]
    )
    await context.bot.create_new_sticker_set(
        admin_id,
        "epd_quotes_by_epd_quotes_bot",
        "EPD Quotes",
        [new_sticker],
        telegram.constants.StickerFormat.STATIC
    )

handler = CommandHandler("admin_create_sticker_pack", admin_create_sticker_pack)