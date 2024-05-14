import telegram
from telegram import Update, constants, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters

from .image_generator import create_quote_image
import os

QUOTE_TEXT, DEFAULT_OR_NEW_AUTHOR, AUTHOR, PREVIEW, DONE = range(5)

chat_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "What quote do you want in a sticker?"
    )
    return QUOTE_TEXT

async def quote_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["yes, it's wuping", "no, it's someone else this time"]]
    chat_data[update.effective_chat.id] = { "quote": update.message.text }
    await update.message.reply_text(
        "Is this from everyone's favourite prof, or is it someone else?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    return DEFAULT_OR_NEW_AUTHOR


async def new_author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Who said this?"
    )

    return PREVIEW

async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = update.message.text
    chat_id = update.effective_chat.id
    print(chat_data)
    print(chat_data[chat_id])
    if reply != "yes, it's wuping":
        chat_data[chat_id]["author"] = update.message.text
    file_name = os.path.join(".", "temp", f"{update.effective_chat.id}.png")
    quote = chat_data[chat_id]["quote"]

    if chat_data[chat_id].get("author") is not None:
        create_quote_image(file_name, quote, chat_data[chat_id].get("author"))
    else:
        create_quote_image(file_name, quote)

    await update.message.reply_sticker(file_name)

    reply_keyboard = [["OK", "/cancel"]]

    await update.message.reply_text(
        "This look good? Hit OK to add it to the pack.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )

    return DONE

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_sticker = telegram.InputSticker(
        open(os.path.join(".", "temp", f"{update.effective_chat.id}.png"), "rb"),
        ["💬"],
        format="static"
    )
    await context.bot.add_sticker_to_set(552476029, "epd_quotes_by_epd_quotes_bot", new_sticker)
    sticker_set = await context.bot.get_sticker_set("epd_quotes_by_epd_quotes_bot")
    await update.message.reply_text(
        "Done! Re-add the pack to see it in your sticker menu.",
    )
    await update.message.reply_sticker(
        sticker_set.stickers[-1]
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Cancelled.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

handler = ConversationHandler(
    entry_points=[CommandHandler("new_quote", start)],
    states={
        QUOTE_TEXT: [MessageHandler(filters.TEXT, quote_text)],
        DEFAULT_OR_NEW_AUTHOR: [
            MessageHandler(filters.Regex("^yes, it's wuping$"), preview),
            MessageHandler(filters.Regex("^no, it's someone else this time"), new_author)
        ],
        PREVIEW: [
            MessageHandler(filters.TEXT, preview),
        ],
        DONE: [MessageHandler(filters.Regex("^OK$"), done)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
