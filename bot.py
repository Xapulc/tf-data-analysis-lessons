import os
import logging

from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from stat_problem1 import problem1, \
                          description_generator_problem1, \
                          transformer_variant_problem1_list, \
                          solution_tester_problem1
from stat_problem2 import problem2, \
                          description_generator_problem2, \
                          transformer_variant_problem2_list, \
                          solution_tester_problem2
from hypothesis_testing_problem1 import hyp_problem1, \
                                        description_generator_hyp_problem1, \
                                        transformer_variant_hyp_problem1_list, \
                                        solution_tester_hyp_problem1
from hypothesis_testing_problem2 import hyp_problem2, \
                                        description_generator_hyp_problem2, \
                                        transformer_variant_hyp_problem2_list, \
                                        solution_tester_hyp_problem2
from hypothesis_testing_problem3 import hyp_problem3, \
                                        description_generator_hyp_problem3, \
                                        transformer_variant_hyp_problem3_list, \
                                        solution_tester_hyp_problem3
from tools import ProblemStorage, \
                  DescriptionGeneratorStrategies, \
                  UserVariantResolver, \
                  Converter, \
                  VariantTransformerStrategies, \
                  SolutionTesterStrategies


problem_storage = ProblemStorage([
    problem1,
    problem2,
    hyp_problem1,
    hyp_problem2,
    hyp_problem3
])
description_generator_strategies = DescriptionGeneratorStrategies([
    description_generator_problem1,
    description_generator_problem2,
    description_generator_hyp_problem1,
    description_generator_hyp_problem2,
    description_generator_hyp_problem3
])
solution_tester_strategies = SolutionTesterStrategies([
    solution_tester_problem1,
    solution_tester_problem2,
    solution_tester_hyp_problem1,
    solution_tester_hyp_problem2,
    solution_tester_hyp_problem3
])
transformer_variant_strategies = VariantTransformerStrategies(transformer_variant_problem1_list
                                                              + transformer_variant_problem2_list
                                                              + transformer_variant_hyp_problem1_list
                                                              + transformer_variant_hyp_problem2_list
                                                              + transformer_variant_hyp_problem3_list)

user_variant_resolver = UserVariantResolver(os.getenv("SOLVER_RANDOM_STATE"))
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

        await context.bot.send_message(chat_id=chat_id,
                                       text=problem.name)

        random_state = user_variant_resolver.get_number(chat_id, problem)
        description_generator = description_generator_strategies.get_description_generator_strategy_by_code(problem.code)
        solution_tester = solution_tester_strategies.get_solution_tester_strategy_by_code(problem.code)

        problem_variant = user_variant_resolver.get_variant(chat_id, problem)
        transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)

        generated_criteria_list = solution_tester.generate_criteria(transformer_variant, random_state)
        description = description_generator.get_description(transformer_variant, generated_criteria_list, random_state)
        if isinstance(description, str):
            description = [description]
        image_path_list = converter.convert_tex_body_str_to_image_list(description[0])

        await context.bot.send_media_group(chat_id=chat_id,
                                           media=[
                                               InputMediaPhoto(open(image_path, "rb"),
                                                               caption="Условие задачи" if i == 0 else "")
                                               for i, image_path in enumerate(image_path_list)
                                           ])

        if len(description) > 1:
            for i, file_path in enumerate(description[1]):
                await context.bot.send_document(chat_id=chat_id,
                                                document=file_path)
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
