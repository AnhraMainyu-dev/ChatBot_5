from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BACK_BUTTON = InlineKeyboardButton("Назад", callback_data="back")


def menu_keyboard(menu):
    keyboard = [
        [InlineKeyboardButton(item["Name"], callback_data=f"id_{item['documentId']}")]
        for item in menu
    ]
    show_cart_button = InlineKeyboardButton(
        "Показать корзину", callback_data="show_cart"
    )
    keyboard.append([show_cart_button])

    return InlineKeyboardMarkup(keyboard)


def add_to_cart_keyboard(item_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Добавить в корзину", callback_data=f"add_id_{item_id}"
                )
            ],
            [BACK_BUTTON],
        ]
    )


def cart_keyboard(cart):
    keyboard = [
        [
            InlineKeyboardButton(
                item["ryba"]["Name"], callback_data=f"id_{item['ryba']['documentId']}"
            ),
            InlineKeyboardButton(
                "Убрать из корзины",
                callback_data=f"delete_cart_item_id_{item['documentId']}",
            ),
        ]
        for item in cart
    ]
    finish_order_button = InlineKeyboardButton("Оплатить", callback_data="finish_order")
    keyboard.append([finish_order_button])
    keyboard.append([BACK_BUTTON])

    return InlineKeyboardMarkup(keyboard)
