import os
import logging
import pytz

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
                  SolutionTesterStrategies, \
                  ActionRun


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


def get_run(action_run, teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        username = " ".join(context.args).strip(" ")

        if len(username) == 0:
            await context.bot.send_message(chat_id=chat_id,
                                           text="При вызове команды укажите свой username в GitHub. "
                                                + "Пример: `/get_run username`.",
                                           parse_mode="markdown")
            return

        res = action_run.get_run_dict(username)
        if res is None:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Не удалось найти запуски для `username = {username}`.",
                                           parse_mode="markdown")
            return

        res_list = [
            res_id
            for res_id in res.values()
        ]
        res_list = sorted(res_list, key=lambda x: x["create_dttm"], reverse=True)

        for res_item in res_list:
            create_dttm = res_item["create_dttm"]
            create_dttm = create_dttm.replace(tzinfo=pytz.utc) \
                                     .astimezone(pytz.timezone("Europe/Moscow")) \
                                     .strftime("%H:%M:%S %d.%m.%Y")
            conclusion = res_item["conclusion"]
            conclusion = "---" if conclusion is None else conclusion

            res_desc = f"* время создания: {create_dttm}\n" \
                       + f"* статус: {res_item['status']}\n" \
                       + f"* итог обработки: {conclusion}\n" \
                       + f"* проект: {res_item['project']}\n"

            if chat_id in teacher_chat_list:
                res_desc += f"\n* запуск: {res_item['run']}"

            await context.bot.send_message(chat_id=chat_id,
                                           text=res_desc)

    return helper


def get_chat(replace_chat_dict=None):
    if replace_chat_dict is None:
        replace_chat_dict = dict()

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        return_chat_id = replace_chat_dict.get(chat_id, chat_id)
        await context.bot.send_message(chat_id=chat_id,
                                       text=return_chat_id)

    return helper


def get_problem_variant_by_code(code, silence_mode_flg=False, silence_mode_white_list=None):
    problem = problem_storage.get_problem_by_code(code)
    if silence_mode_white_list is None:
        silence_mode_white_list = []
    
    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in silence_mode_white_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"{problem.name}. Генерация условия недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"{problem.name}. Генерация условия...")
            try:
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
            except Exception as e:
                comment = "Ошибка при генерации условия. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_problem_variant_solution_by_code(code, silence_mode_flg=False, silence_mode_white_list=None):
    problem = problem_storage.get_problem_by_code(code)
    if silence_mode_white_list is None:
        silence_mode_white_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in silence_mode_white_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"{problem.name}. Генерация решения недоступна.")
        elif problem.code not in (problem1.code, problem2.code):
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"{problem.name}. Генерация решения недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"{problem.name}. Генерация решения...")
            try:
                random_state = user_variant_resolver.get_number(chat_id, problem)
                description_generator = description_generator_strategies.get_description_generator_strategy_by_code(problem.code)
                solution_tester = solution_tester_strategies.get_solution_tester_strategy_by_code(problem.code)

                problem_variant = user_variant_resolver.get_variant(chat_id, problem)
                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)

                generated_criteria_list = solution_tester.generate_criteria(transformer_variant, random_state)
                description = description_generator.get_solution_description(transformer_variant, generated_criteria_list, random_state)
                if isinstance(description, str):
                    description = [description]
                image_path_list = converter.convert_tex_body_str_to_image_list(description[0])

                await context.bot.send_media_group(chat_id=chat_id,
                                                   media=[
                                                       InputMediaPhoto(open(image_path, "rb"),
                                                                       caption="Решение задачи" if i == 0 else "")
                                                       for i, image_path in enumerate(image_path_list)
                                                   ])

                if len(description) > 1:
                    for i, file_path in enumerate(description[1]):
                        await context.bot.send_document(chat_id=chat_id,
                                                        document=file_path)
            except Exception as e:
                comment = "Ошибка при генерации решения. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    action_run = ActionRun(os.getenv("GITHUB_TOKEN"))
    action_run.start()
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_chat", get_chat({604918251: 123456})))

    for problem in problem_storage.problem_list:
        code = problem.code
        application.add_handler(CommandHandler(f"get_{code}",
                                               get_problem_variant_by_code(code,
                                                                           silence_mode_flg=False,
                                                                           silence_mode_white_list=[
                                                                               604918251
                                                                           ])))
        application.add_handler(CommandHandler(f"get_solution_{code}",
                                               get_problem_variant_solution_by_code(code,
                                                                                    silence_mode_flg=False,
                                                                                    silence_mode_white_list=[
                                                                                        604918251
                                                                                    ])))
    application.add_handler(CommandHandler("get_run", get_run(action_run,
                                                              teacher_chat_list=[
                                                                  604918251
                                                              ])))
    application.run_polling()
