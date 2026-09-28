from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from tg_bot.strapi_requests import fetch_singular_item, fetch_content_type

BACK_BUTTON = InlineKeyboardButton("Назад", callback_data="back")

def menu_keyboard(menu):
    keyboard = [
        [InlineKeyboardButton(item['name'], callback_data=f"id_{item['id']}")]
        for item in menu
    ]
    show_cart_button = InlineKeyboardButton('Показать корзину', callback_data="show_cart")
    keyboard.append([show_cart_button])

    return InlineKeyboardMarkup(keyboard)


def add_to_cart_keyboard(item_id):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Добавить в корзину", callback_data=f"add_id_{item_id}")],
            BACK_BUTTON
        ]
    )

def cart_keyboard(cart):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(item['name'], callback_data=f'cart_item_id{item['id']}'),
                InlineKeyboardButton('Убрать из корзины', callback_data=f'delete_cart_item_id_{item['id']}'),
            ]
            for item in cart
        ]
    )