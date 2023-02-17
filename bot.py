import os
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from utils import get_variant
from stat_task1.test import salt as stat_task1_salt, \
                min_variant as stat_task1_min_variant, \
                            max_variant as stat_task1_max_variant
from stat_task2.test import salt as stat_task2_salt, \
                min_variant as stat_task2_min_variant, \
                            max_variant as stat_task2_max_variant


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                   text='Я бот для поддержки курса "Анализ данных в индустрии". '
                    + 'Для выполнения ДЗ вам потребуется `chat_id`. '
                        + f'Ваш `chat_id` равен {update.effective_chat.id}.',
                   parse_mode="markdown")


async def get_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                   text=update.effective_chat.id)


def get_variant_by_task(task_name):
    get_variant_by_id = None
    if task_name == stat_task1_salt:
        get_variant_by_id = lambda id: get_variant(id, 
                                                   stat_task1_salt,
                                                   stat_task1_min_variant,
                                                   stat_task1_max_variant)
    elif task_name == stat_task2_salt:
        get_variant_by_id = lambda id: get_variant(id, 
                                                   stat_task2_salt,
                                                   stat_task2_min_variant,
                                                   stat_task2_max_variant)
    
    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=get_variant_by_id(update.effective_chat.id))
    return helper


if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_chat", get_chat))

    for task_name in [stat_task1_salt, 
                      stat_task2_salt]:
        application.add_handler(CommandHandler(f"get_variant_{task_name}", get_variant_by_task(task_name)))
    
    application.run_polling()
