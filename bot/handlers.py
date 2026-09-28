from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import Forbidden
from telegram.ext import ContextTypes, ConversationHandler

START, HANDLE_MENU, HANDLE_DESCRIPTION, SHOW_ORDER, COMPLETE_ORDER = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please choose:"
    )
