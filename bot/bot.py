import telegram
from decouple import config
from telegram.ext import CallbackContext, Application,CommandHandler,ConversationHandler,MessageHandler,CallbackQueryHandler, filters

def main():
    app = Application.builder().token(config('TG_API_KEY')).build()

if __name__ == '__main__':
    main()