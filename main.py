import re

from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, Updater,
)
import logging
from constants import *
from functions import *


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def first_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Привет! Я проект Орлова Андрея', reply_markup=ReplyKeyboardMarkup([['Привет']]))
    return START

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Что вы хотите?', reply_markup=ReplyKeyboardMarkup([start_keyboard]))
    return DESCRIPTION

async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    if update.message.text == start_keyboard[0]: # Описание
        logger.info("%s выбрал категорию %s", user.first_name, update.message.text)
        await update.message.reply_text('Данный бот пользуется данными с ресурса nebo.live, чтобы в удобной форме донести до вас можно ли безопасно выходить на улицу')
        return DESCRIPTION
    elif update.message.text == start_keyboard[1]: # Начало работы
        logger.info("%s выбрал категорию %s", user.first_name, update.message.text)
        await update.message.reply_text('Выберите интересующий вас район', reply_markup=ReplyKeyboardMarkup(district_keyboard, one_time_keyboard=True))
        return DISTRICT

async def district(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s выбрал категорию %s", user.first_name, update.message.text)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', first_message)],
        states={
            START: [MessageHandler(filters.Regex('Привет|Описание'), start)],
            DESCRIPTION: [MessageHandler(filters.Regex('|'.join(make_regex_string(start_keyboard.copy()))), description)],
            DISTRICT: [MessageHandler(filters.Regex('|'.join(make_regex_string(district_keyboard.copy()))), district)]
        },
        fallbacks=[MessageHandler(filters.Regex(re.compile('Назад|Cancel', re.IGNORECASE)), cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.run_polling()
    logging.info('Stopped server')
    return 0

if __name__ == '__main__':
    main()