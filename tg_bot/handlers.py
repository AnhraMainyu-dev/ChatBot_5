from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import Forbidden
from telegram.ext import ContextTypes, ConversationHandler
from keyboards import menu_keyboard, add_to_cart_keyboard, cart_keyboard
from tg_bot.strapi_requests import fetch_singular_item, fetch_content_type, add_to_cart, fetch_cart, delete_from_cart
from decouple import config

START, WAIT_ITEM, WAIT_DESCRIPTION, SHOW_CART, COMPLETE_ORDER = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = fetch_content_type('lososes', config('STRAPI_API'))
    await update.effective_message.reply_text(
        "Please choose:",
        reply_markup=menu_keyboard(menu)
    )

    return WAIT_ITEM

async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item_id = query.data.removeprefix("id_")
    item = fetch_singular_item('lososes', config('STRAPI_API'), int(item_id))
    await update.message.reply_text(
        item['Description'],
        reply_markup=add_to_cart_keyboard(id)
    )

    return WAIT_DESCRIPTION

async def handle_add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item_id = query.data.removeprefix("add_id_")
    add_to_cart(item_id, config('STRAPI_API'))
    await update.message.reply_text(
        "Добавлено!",
        reply_markup=add_to_cart_keyboard(id)
    )

    return WAIT_DESCRIPTION


async def handle_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart = fetch_cart(context.user_id, config('STRAPI_API'))
    await update.message.reply_text(
        "Товары в корзине:",
        reply_markup=cart_keyboard(cart)
    )

    return SHOW_CART

async def handle_delete_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item_id = query.data.removeprefix("delete_cart_item_id_")
    delete_from_cart(item_id, config('STRAPI_API'))

    return SHOW_CART



async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    return await start(update, context)
