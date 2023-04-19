import os
import logging

import pandas as pd
import pytz
import numpy as np

from scipy.stats import randint, ks_2samp, anderson_ksamp, cramervonmises_2samp
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
from telesales_project import telesales, \
                              telesales_project, \
                              transformer_telesales_project_list
from credit_card_project import credit_card, \
                                credit_card_project, \
                                transformer_credit_card_project_list
from unbalanced_sample import unbalanced_sample, \
                              transformer_unbalanced_sample_list
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
                                                              + transformer_variant_hyp_problem3_list
                                                              + transformer_telesales_project_list
                                                              + transformer_credit_card_project_list
                                                              + transformer_unbalanced_sample_list)

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


def get_telesales_project_description(silence_mode_flg=False, teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in teacher_chat_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text="Генерация условия недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация условия...")
            try:
                if chat_id in teacher_chat_list:
                    student_chat_id = int(" ".join(context.args).strip(" "))
                else:
                    student_chat_id = chat_id

                random_state = user_variant_resolver.get_number(student_chat_id, telesales_project)
                problem_variant = user_variant_resolver.get_variant(student_chat_id, telesales_project)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)
                description = transformer_variant.get_description(random_state)

                await context.bot.send_message(chat_id=chat_id, text=description, parse_mode="markdown")

                hist_data = telesales.generate_sample(sample_size=telesales.sample_size,
                                                      random_state=telesales.random_state)
                file_name = "tmp/hist_telesales.csv"
                hist_data.to_csv(file_name, index=False)
                await context.bot.send_document(chat_id=chat_id,
                                                caption="Исторические данные",
                                                document=file_name)
            except Exception as e:
                comment = "Ошибка при генерации условия. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_telesales_project_sample(silence_mode_flg=False, teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in teacher_chat_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text="Генерация выборки недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация выборки...")
            sample_size = " ".join(context.args).strip(" ")
            if len(sample_size) == 0:
                await context.bot.send_message(chat_id=chat_id,
                                               text="Заполните размер выборки в формате `/get_project1_sample {размер выборки}`",
                                               parse_mode="markdown")
                return

            try:
                sample_size = int(sample_size)
                assert sample_size > 0, "Неположительный разер выборки"
                assert sample_size <= 1000000, "Cлишком большая выборка"
            except Exception as e:
                comment = "Ошибка при распозновании размера выборки. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}."
                await context.bot.send_message(chat_id=chat_id, text=comment)
                return

            try:
                random_state = user_variant_resolver.get_number(chat_id, telesales_project)
                problem_variant = user_variant_resolver.get_variant(chat_id, telesales_project)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)

                sample_random_state = randint.rvs(124, 43251)
                control_data, test_data = telesales.generate_test_sample(sample_size,
                                                                         transformer_variant.get_metric(),
                                                                         transformer_variant.get_alternative(),
                                                                         transformer_variant.relative_mde,
                                                                         sample_random_state)

                for sample, sample_desc in zip([control_data, test_data], ["Контроль", "Тест"]):
                    file_name = f"tmp/{sample_desc}.csv"
                    sample.to_csv(file_name, index=False)
                    await context.bot.send_document(chat_id=chat_id,
                                                    caption=f"Выборка '{sample_desc}'",
                                                    document=file_name)

                await context.bot.send_message(chat_id=chat_id,
                                               text=f"Код выборки: `{sample_random_state}`.",
                                               parse_mode="markdown")
            except Exception as e:
                comment = "Ошибка при генерации выборки. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_telesales_project_report(teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if chat_id in teacher_chat_list:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация отчёта...")

            try:
                student_chat_id = int(context.args[0])
                sample_random_state = int(context.args[1])
                sample_size = int(context.args[2])

                random_state = user_variant_resolver.get_number(student_chat_id, telesales_project)
                problem_variant = user_variant_resolver.get_variant(student_chat_id, telesales_project)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)
                description = transformer_variant.get_description(random_state)
                await context.bot.send_message(chat_id=chat_id, text=description, parse_mode="markdown")

                hist_data = telesales.generate_sample(sample_size=telesales.sample_size,
                                                      random_state=telesales.random_state)
                target_column = hist_data[transformer_variant.get_metric()]
                await context.bot.send_message(chat_id=chat_id,
                                               text=f"Целевая метрика: {transformer_variant.get_metric()}.\n"
                                                    + f"Альтернатива: '{transformer_variant.get_alternative()}'.\n"
                                                    + f"Выборочное среднее: {target_column.mean():.2f}.\n"
                                                    + f"Выборочная дисперсия: {target_column.var():.2f}.")

                control_sample_size, test_sample_size = telesales.get_sample_size(transformer_variant.get_metric(),
                                                                                  transformer_variant.get_alternative(),
                                                                                  transformer_variant.alpha,
                                                                                  transformer_variant.beta,
                                                                                  transformer_variant.relative_mde)
                dev_sample_size = np.abs(sample_size / control_sample_size - 1)
                await context.bot.send_message(chat_id=chat_id,
                                               text=f"Размер выборки на контроле: {control_sample_size:.0f}.\n"
                                                    + f"Размер выборки на тесте: {test_sample_size:.0f}.\n"
                                                    + f"Отклонение от истинного значения: {dev_sample_size:.1%}")

                control_data, test_data = telesales.generate_test_sample(sample_size,
                                                                         transformer_variant.get_metric(),
                                                                         transformer_variant.get_alternative(),
                                                                         transformer_variant.relative_mde,
                                                                         sample_random_state)
                control_sample = control_data[transformer_variant.get_metric()]
                test_sample = test_data[transformer_variant.get_metric()]
                p = transformer_variant.check_homogeneity(control_sample, test_sample)
                hypothesis_desc = "H(0)" if telesales.get_hypothesis(sample_random_state) else "H(1)"

                await context.bot.send_message(chat_id=chat_id,
                                               text=f"p-value критерия: {p:.3f}. "
                                                    + f"Справедлива {hypothesis_desc}")
            except Exception as e:
                comment = "Ошибка при генерации отчёта. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_credit_card_project_description(silence_mode_flg=False, teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in teacher_chat_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text="Генерация условия недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация условия...")
            try:
                if chat_id in teacher_chat_list:
                    student_chat_id = int(" ".join(context.args).strip(" "))
                else:
                    student_chat_id = chat_id

                random_state = user_variant_resolver.get_number(student_chat_id, credit_card_project)
                problem_variant = user_variant_resolver.get_variant(student_chat_id, credit_card_project)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)
                description = transformer_variant.get_description(random_state)

                await context.bot.send_message(chat_id=chat_id, text=description, parse_mode="markdown")

                hist_data = credit_card.generate_sample(sample_size=credit_card.sample_size,
                                                        random_state=credit_card.random_state)
                file_name = "tmp/hist_credit_card.csv"
                hist_data.to_csv(file_name, index=False)
                await context.bot.send_document(chat_id=chat_id,
                                                caption="Исторические данные",
                                                document=file_name)
            except Exception as e:
                comment = "Ошибка при генерации условия. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_credit_card_project_sample(silence_mode_flg=False, teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in teacher_chat_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text="Генерация выборки недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация выборки...")
            sample_size = " ".join(context.args).strip(" ")
            if len(sample_size) == 0:
                await context.bot.send_message(chat_id=chat_id,
                                               text="Заполните размер выборки в формате `/get_project2_sample {размер выборки}`",
                                               parse_mode="markdown")
                return

            try:
                sample_size = int(sample_size)
                assert sample_size > 0, "Неположительный разер выборки"
                assert sample_size <= 1000000, "Cлишком большая выборка"
            except Exception as e:
                comment = "Ошибка при распозновании размера выборки. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}."
                await context.bot.send_message(chat_id=chat_id, text=comment)
                return

            try:
                random_state = user_variant_resolver.get_number(chat_id, credit_card_project)
                problem_variant = user_variant_resolver.get_variant(chat_id, credit_card_project)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)

                sample_random_state = randint.rvs(414, 79080)
                control_data, test_data = credit_card.generate_test_sample(sample_size,
                                                                           transformer_variant.get_metric(),
                                                                           transformer_variant.get_alternative(),
                                                                           transformer_variant.relative_mde,
                                                                           sample_random_state)

                for sample, sample_desc in zip([control_data, test_data], ["Контроль", "Тест"]):
                    file_name = f"tmp/{sample_desc}.csv"
                    sample.to_csv(file_name, index=False)
                    await context.bot.send_document(chat_id=chat_id,
                                                    caption=f"Выборка '{sample_desc}'",
                                                    document=file_name)

                await context.bot.send_message(chat_id=chat_id,
                                               text=f"Код выборки: `{sample_random_state}`.",
                                               parse_mode="markdown")
            except Exception as e:
                comment = "Ошибка при генерации выборки. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_credit_card_project_report(teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if chat_id in teacher_chat_list:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация отчёта...")

            try:
                student_chat_id = int(context.args[0])
                sample_random_state = int(context.args[1])
                sample_size = int(context.args[2])

                random_state = user_variant_resolver.get_number(student_chat_id, credit_card_project)
                problem_variant = user_variant_resolver.get_variant(student_chat_id, credit_card_project)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)
                description = transformer_variant.get_description(random_state)
                await context.bot.send_message(chat_id=chat_id, text=description, parse_mode="markdown")

                hist_data = credit_card.generate_sample(sample_size=credit_card.sample_size,
                                                        random_state=credit_card.random_state)
                target_column = hist_data[transformer_variant.get_metric()]
                await context.bot.send_message(chat_id=chat_id,
                                               text=f"Целевая метрика: {transformer_variant.get_metric()}.\n"
                                                    + f"Альтернатива: '{transformer_variant.get_alternative()}'.\n"
                                                    + f"Выборочное среднее: {target_column.mean():.2f}.\n"
                                                    + f"Выборочная дисперсия: {target_column.var():.2f}.")

                control_sample_size, test_sample_size = credit_card.get_sample_size(transformer_variant.get_metric(),
                                                                                    transformer_variant.get_alternative(),
                                                                                    transformer_variant.alpha,
                                                                                    transformer_variant.beta,
                                                                                    transformer_variant.relative_mde)
                dev_sample_size = np.abs(sample_size / control_sample_size - 1)
                await context.bot.send_message(chat_id=chat_id,
                                               text=f"Размер выборки на контроле: {control_sample_size:.0f}.\n"
                                                    + f"Размер выборки на тесте: {test_sample_size:.0f}.\n"
                                                    + f"Отклонение от истинного значения: {dev_sample_size:.1%}")

                control_data, test_data = credit_card.generate_test_sample(sample_size,
                                                                           transformer_variant.get_metric(),
                                                                           transformer_variant.get_alternative(),
                                                                           transformer_variant.relative_mde,
                                                                           sample_random_state)
                control_homo_sample = control_data[credit_card.homo_check_metric_name]
                test_homo_sample = test_data[credit_card.homo_check_metric_name]
                message = f"Параметр для проверки однородности: `{credit_card.homo_check_metric_name}`.\n"

                if credit_card.get_homo_hypothesis(sample_random_state):
                    message += "Выборки однородны."
                else:
                    message += "\nВыборки неоднородны."

                homo_test_list = [{
                    "name": "Колмогоров-Смирнов",
                    "pvalue": lambda x, y: ks_2samp(x, y, alternative="two-sided").pvalue
                }, {
                    "name": "Андерсон-Дарлинг",
                    "pvalue": lambda x, y: anderson_ksamp([x, y]).pvalue
                }, {
                    "name": "CVM",
                    "pvalue": lambda x, y: cramervonmises_2samp(x, y).pvalue
                }]

                for test in homo_test_list:
                    p = test["pvalue"](control_homo_sample, test_homo_sample)
                    message += f"\nКритерий: `{test['name']}`, p-value: `{p:.3f}`."

                await context.bot.send_message(chat_id=chat_id,
                                               text=message,
                                               parse_mode="markdown")

                control_sample = control_data[transformer_variant.get_metric()]
                test_sample = test_data[transformer_variant.get_metric()]
                p = transformer_variant.check_homogeneity(control_sample, test_sample)
                hypothesis_desc = "H(0)" if credit_card.get_hypothesis(sample_random_state) else "H(1)"

                await context.bot.send_message(chat_id=chat_id,
                                               text=f"p-value критерия: {p:.3f}. "
                                                    + f"Справедлива {hypothesis_desc}")
            except Exception as e:
                comment = "Ошибка при генерации отчёта. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`."
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
        elif problem.code not in (problem1.code, problem2.code,
                                  hyp_problem1.code, hyp_problem2.code, hyp_problem3.code):
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

                if description[0] is not None:
                    image_path_list = converter.convert_tex_body_str_to_image_list(description[0])

                    await context.bot.send_media_group(chat_id=chat_id,
                                                       media=[
                                                           InputMediaPhoto(open(image_path, "rb"),
                                                                           caption="Решение задачи" if i == 0 else "")
                                                           for i, image_path in enumerate(image_path_list)
                                                       ])

                if len(description) > 1:
                    for message in description[1:]:
                        await context.bot.send_message(chat_id=chat_id,
                                                       text=message,
                                                       parse_mode="markdown")
            except Exception as e:
                comment = "Ошибка при генерации решения. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_unbalanced_sample_description(silence_mode_flg=False, teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if silence_mode_flg and (chat_id not in teacher_chat_list):
            await context.bot.send_message(chat_id=chat_id,
                                           text="Генерация условия недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация условия...")
            try:
                if chat_id in teacher_chat_list:
                    student_chat_id = int(" ".join(context.args).strip(" "))
                else:
                    student_chat_id = chat_id

                random_state = user_variant_resolver.get_number(student_chat_id, unbalanced_sample)
                problem_variant = user_variant_resolver.get_variant(student_chat_id, unbalanced_sample)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)
                description = transformer_variant.get_description(random_state)

                await context.bot.send_message(chat_id=chat_id, text=description, parse_mode="markdown")

                hist_sample = transformer_variant.get_sample(random_state=random_state)
                hist_data = pd.DataFrame(data={
                    f"x{i+1}": [x]
                    for i, x in enumerate(hist_sample)
                })
                file_name = "tmp/hist_unbalanced_sample.csv"
                hist_data.to_csv(file_name, index=False)
                await context.bot.send_document(chat_id=chat_id,
                                                caption="Исторические данные",
                                                document=file_name)
            except Exception as e:
                comment = "Ошибка при генерации условия. " \
                          + f"Тип ошибки: {type(e)}, сообщение: {str(e)}, `chat_id = {str(chat_id)}`. " \
                          + f"Перешлите это сообщение преподавателю."
                await context.bot.send_message(chat_id=chat_id, text=comment)

    return helper


def get_unbalanced_sample_report(teacher_chat_list=None):
    if teacher_chat_list is None:
        teacher_chat_list = []

    async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if chat_id not in teacher_chat_list:
            await context.bot.send_message(chat_id=chat_id,
                                           text="Генерация условия недоступна.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Генерация условия...")
            try:
                student_chat_id = int(" ".join(context.args).strip(" "))

                random_state = user_variant_resolver.get_number(student_chat_id, unbalanced_sample)
                problem_variant = user_variant_resolver.get_variant(student_chat_id, unbalanced_sample)

                transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)
                description = transformer_variant.get_description(random_state)

                await context.bot.send_message(chat_id=chat_id, text=description, parse_mode="markdown")

                hist_sample = transformer_variant.get_sample(random_state=random_state)
                hist_data = pd.DataFrame(data={
                    f"x{i+1}": [x]
                    for i, x in enumerate(hist_sample)
                })
                file_name = "tmp/hist_unbalanced_sample.csv"
                hist_data.to_csv(file_name, index=False)
                await context.bot.send_document(chat_id=chat_id,
                                                caption="Исторические данные",
                                                document=file_name)

                solution_description = transformer_variant.get_solution_description(random_state)

                await context.bot.send_message(chat_id=chat_id, text=solution_description, parse_mode="markdown")
            except Exception as e:
                comment = "Ошибка при генерации условия. " \
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

    teacher_chat_list = [
        604918251
    ]

    for problem in problem_storage.problem_list:
        code = problem.code
        application.add_handler(CommandHandler(f"get_{code}",
                                               get_problem_variant_by_code(code,
                                                                           silence_mode_flg=False,
                                                                           silence_mode_white_list=teacher_chat_list)))
        application.add_handler(CommandHandler(f"get_solution_{code}",
                                               get_problem_variant_solution_by_code(code,
                                                                                    silence_mode_flg=False,
                                                                                    silence_mode_white_list=teacher_chat_list)))
    application.add_handler(CommandHandler("get_run", get_run(action_run,
                                                              teacher_chat_list=teacher_chat_list)))

    application.add_handler(CommandHandler("get_unbalanced_desc",
                                           get_unbalanced_sample_description(silence_mode_flg=False,
                                                                             teacher_chat_list=teacher_chat_list)))
    application.add_handler(CommandHandler("get_unbalanced_report",
                                           get_unbalanced_sample_report(teacher_chat_list=teacher_chat_list)))

    project_teacher_chat_list = [
        604918251,  # Витя
        434207209,  # Ангелина
        123188318,  # Андрей,
        315763504,  # Коля
        957195795,  # Максим
    ]

    application.add_handler(CommandHandler("get_project1_desc",
                                           get_telesales_project_description(silence_mode_flg=False,
                                                                             teacher_chat_list=project_teacher_chat_list)))
    application.add_handler(CommandHandler("get_project1_sample",
                                           get_telesales_project_sample(silence_mode_flg=False,
                                                                        teacher_chat_list=project_teacher_chat_list)))
    application.add_handler(CommandHandler("get_project1_report",
                                           get_telesales_project_report(teacher_chat_list=project_teacher_chat_list)))
    application.add_handler(CommandHandler("get_project2_desc",
                                           get_credit_card_project_description(silence_mode_flg=False,
                                                                               teacher_chat_list=project_teacher_chat_list)))
    application.add_handler(CommandHandler("get_project2_sample",
                                           get_credit_card_project_sample(silence_mode_flg=False,
                                                                          teacher_chat_list=project_teacher_chat_list)))
    application.add_handler(CommandHandler("get_project2_report",
                                           get_credit_card_project_report(teacher_chat_list=project_teacher_chat_list)))
    application.run_polling()
