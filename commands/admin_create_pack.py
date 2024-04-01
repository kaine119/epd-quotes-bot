import telegram
from telegram import Update, constants, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters

config = {}

def set_config(file_config):
    global config
    config = file_config

async def admin_create_sticker_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message.from_user.id != config['admin_id']):
        await update.message.reply_text("Admin-only command. Sorry!")
        return
    new_sticker = telegram.InputSticker(
        open("./test.png", "rb"),
        ["🧪"]
    )
    await context.bot.create_new_sticker_set(
        config['admin_id'],
        config['pack_name'],
        config['pack_titles'],
        [new_sticker],
        telegram.constants.StickerFormat.STATIC
    )

handler = CommandHandler("admin_create_sticker_pack", admin_create_sticker_pack)