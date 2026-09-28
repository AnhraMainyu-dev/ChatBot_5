from decouple import config
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from tg_bot.keyboards import (BACK_BUTTON, add_to_cart_keyboard, cart_keyboard,
                              menu_keyboard)
from tg_bot.strapi_requests import (add_to_cart, create_cart, delete_from_cart,
                                    fetch_cart, fetch_cart_id,
                                    fetch_content_type, fetch_picture,
                                    fetch_singular_item, send_order)

WAIT_ITEM = "Searching menu"
WAIT_DESCRIPTION = "Reading description"
SHOW_CART = "Looking at cart"
WAIT_MAIL = "Paying"  # sending mail тут


def save_state(update, context, state):
    db = context.bot_data["db"]
    db.set(update.effective_chat.id, state)
    return state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = fetch_content_type("lososes", config("STRAPI_API"))

    if "cart_id" not in context.user_data:
        tg_id = update.effective_user.id
        cart_id = fetch_cart_id(tg_id, config("STRAPI_API"))
        if cart_id is None:
            cart_id = create_cart(tg_id, config("STRAPI_API"))
        context.user_data["cart_id"] = cart_id

    await update.effective_message.reply_text(
        "Please choose:", reply_markup=menu_keyboard(menu)
    )

    return save_state(update, context, WAIT_ITEM)


async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.delete()

    item_id = query.data.removeprefix("id_")
    item = fetch_singular_item("lososes", item_id, config("STRAPI_API"))
    item_image = fetch_picture(item)

    await update.effective_message.reply_photo(
        photo=item_image,
        caption=item["Description"],
        reply_markup=add_to_cart_keyboard(item_id),
    )

    return save_state(update, context, WAIT_DESCRIPTION)


async def handle_add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    item_id = query.data.removeprefix("add_id_")
    add_to_cart(
        update.effective_user.id,
        context.user_data["cart_id"],
        item_id,
        config("STRAPI_API"),
    )
    await query.answer("Добавлено!")

    return save_state(update, context, WAIT_DESCRIPTION)


async def handle_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart = fetch_cart(context.user_data["cart_id"], config("STRAPI_API"))
    await query.edit_message_text("Товары в корзине:", reply_markup=cart_keyboard(cart))

    return save_state(update, context, SHOW_CART)


async def handle_delete_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cart_item_id = update.callback_query.data.removeprefix("delete_cart_item_id_")
    delete_from_cart(cart_item_id, config("STRAPI_API"))

    return await handle_cart(update, context)


async def accept_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "Заказ принят. Пожалуйста укажите вашу почту",
        reply_markup=InlineKeyboardMarkup([[BACK_BUTTON]]),
    )

    return save_state(update, context, WAIT_MAIL)


async def finish_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    send_order(
        email,
        update.effective_user.full_name,
        context.user_data["cart_id"],
        config("STRAPI_API"),
    )
    context.user_data.pop("cart_id", None)

    await update.message.reply_text(
        "Заказ отправлен! С вами свяжутся в ближайшее время"
    )

    return await start(update, context)


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.delete()
    return await start(update, context)
