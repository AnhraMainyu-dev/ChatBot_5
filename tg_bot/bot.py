import telegram
import redis
from decouple import config
from telegram.ext import CallbackContext, Application,CommandHandler,ConversationHandler,MessageHandler,CallbackQueryHandler, filters
from tg_bot.handlers import start, START, WAIT_ITEM, WAIT_DESCRIPTION, SHOW_CART, COMPLETE_ORDER, handle_description, back_to_menu


def main():
    app = Application.builder().token(config('TG_API_KEY')).build()
    db = redis.Redis(host='localhost', port=6379, decode_responses=True)
    app.bot_data["db"] = db

    order_handler =ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAIT_ITEM: [CallbackQueryHandler(handle_description, pattern=r'^id_')],
            WAIT_DESCRIPTION: [
                CallbackQueryHandler(back_to_menu, pattern='^back$'),
                CallbackQueryHandler(back_to_menu, pattern='^back$'),
                ],
            SHOW_CART: [],
            COMPLETE_ORDER: []

        }
    )
if __name__ == '__main__':
    main()