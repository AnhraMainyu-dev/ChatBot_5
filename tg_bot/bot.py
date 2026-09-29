import redis
from decouple import config
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from tg_bot.handlers import (SHOW_CART, WAIT_DESCRIPTION, WAIT_ITEM, WAIT_MAIL,
                             accept_mail, back_to_menu, finish_order,
                             handle_add_to_cart, handle_cart,
                             handle_delete_item, handle_description, start)


def main():
    app = Application.builder().token(config("TG_API_KEY")).build()
    db = redis.Redis(host="localhost", port=6379, decode_responses=True)
    app.bot_data["db"] = db
    app.bot_data['strapi_url'] = config('STRAPI_URL')
    app.bot_data['strapi_api'] = config('STRAPI_API')

    order_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAIT_ITEM: [
                CallbackQueryHandler(handle_description, pattern=r"^id_"),
                CallbackQueryHandler(handle_cart, pattern="^show_cart"),
            ],
            WAIT_DESCRIPTION: [
                CallbackQueryHandler(back_to_menu, pattern="^back$"),
                CallbackQueryHandler(handle_add_to_cart, pattern="^add_id_"),
            ],
            SHOW_CART: [
                CallbackQueryHandler(back_to_menu, pattern="^back$"),
                CallbackQueryHandler(handle_description, pattern=r"^id_"),
                CallbackQueryHandler(
                    handle_delete_item, pattern=r"^delete_cart_item_id_"
                ),
                CallbackQueryHandler(accept_mail, pattern="^finish_order"),
            ],
            WAIT_MAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish_order),
                CallbackQueryHandler(back_to_menu, pattern="^back$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(order_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
