import os
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from stat_problem1 import problem1, \
                          description_generator_problem1, \
                          transformer_variant_problem1_list
from stat_problem2 import problem2, \
                          description_generator_problem2, \
                          transformer_variant_problem2_list
from tools import ProblemStorage, \
                  DescriptionGeneratorStrategies, \
                  UserVariantResolver, \
                  Converter, \
                  VariantTransformerStrategies


problem_storage = ProblemStorage([
    problem1,
    problem2
])
description_generator_strategies = DescriptionGeneratorStrategies([
    description_generator_problem1,
    description_generator_problem2
])
transformer_variant_strategies = VariantTransformerStrategies(transformer_variant_problem1_list
                                                              + transformer_variant_problem2_list)

user_variant_resolver = UserVariantResolver()
converter = Converter()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text='Я бот для поддержки курса "Анализ данных в индустрии". '
                                         + "Для выполнения ДЗ вам потребуется `chat_id`. "
                                         + f"Ваш `chat_id` равен {update.effective_chat.id}.",
                                   parse_mode="markdown")


async def get_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=update.effective_chat.id)


def get_problem_variant_by_code(code):
    problem = problem_storage.get_problem_by_code(code)
    
    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        random_state = user_variant_resolver.get_number(chat_id, problem)
        description_generator = description_generator_strategies.get_description_generator_strategy_by_code(problem.code)

        problem_variant = user_variant_resolver.get_variant(chat_id, problem)
        transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)

        description = description_generator.get_description(transformer_variant, random_state)
        image_path_list = converter.convert_tex_body_str_to_image_list(description)

        await context.bot.send_message(chat_id=chat_id,
                                       text=problem.name)

        for i, image_path in enumerate(image_path_list):
            await context.bot.send_photo(chat_id=chat_id,
                                         caption=f"Страница условия {i}",
                                         photo=image_path)
    return helper


if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_chat", get_chat))

    for problem in problem_storage.problem_list:
        code = problem.code
        application.add_handler(CommandHandler(f"get_{code}",
                                               get_problem_variant_by_code(code)))
    
    application.run_polling()
