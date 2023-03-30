import os

from stat_problem1 import problem1, \
                          result_problem1, \
                          description_generator_problem1, \
                          solution_tester_problem1, \
                          transformer_variant_problem1_list
from stat_problem2 import problem2, \
                          result_problem2, \
                          description_generator_problem2, \
                          solution_tester_problem2, \
                          transformer_variant_problem2_list
from hypothesis_testing_problem1 import hyp_problem1, \
                                        result_hyp_problem1, \
                                        description_generator_hyp_problem1, \
                                        solution_tester_hyp_problem1, \
                                        transformer_variant_hyp_problem1_list
from hypothesis_testing_problem2 import hyp_problem2, \
                                        result_hyp_problem2, \
                                        description_generator_hyp_problem2, \
                                        solution_tester_hyp_problem2, \
                                        transformer_variant_hyp_problem2_list
from hypothesis_testing_problem3 import hyp_problem3, \
                                        result_hyp_problem3, \
                                        description_generator_hyp_problem3, \
                                        solution_tester_hyp_problem3, \
                                        transformer_variant_hyp_problem3_list
from tools import ProblemStorage, \
                  DescriptionGeneratorStrategies, \
                  SolutionTesterStrategies, \
                  ResultStrategies, \
                  EduService, \
                  TelegramService, \
                  UserVariantResolver, \
                  VariantTransformerStrategies


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
result_strategies = ResultStrategies([
    result_problem1,
    result_problem2,
    result_hyp_problem1,
    result_hyp_problem2,
    result_hyp_problem3
])
transformer_variant_strategies = VariantTransformerStrategies(transformer_variant_problem1_list
                                                              + transformer_variant_problem2_list
                                                              + transformer_variant_hyp_problem1_list
                                                              + transformer_variant_hyp_problem2_list
                                                              + transformer_variant_hyp_problem3_list)


if __name__ == "__main__":
    task_id = os.getenv("task_id")
    pull_req_url = os.getenv("pull_req_url")
    problem = problem_storage.get_problem_by_task_id(task_id)

    result_strategy = result_strategies.get_result_strategy_by_code(problem.code)
    description_generator = description_generator_strategies.get_description_generator_strategy_by_code(problem.code)
    solution_tester = solution_tester_strategies.get_solution_tester_strategy_by_code(problem.code)

    edu_service = EduService(env_file=os.getenv("GITHUB_ENV"))
    telegram_service = TelegramService(token=os.getenv("TELEGRAM_TOKEN"))
    user_variant_resolver = UserVariantResolver(os.getenv("SOLVER_RANDOM_STATE"))

    try:
        from student_work.solution import chat_id
    except ImportError as e:
        comment = "Chat ID не указан"
        print(comment)

        for teacher_chat_id in problem.teacher_chat_id_list:
            teacher_messange = f"`{problem.name}` проверено, " \
                               + f"проект: `{pull_req_url}`.\n" \
                               + f"В решении следующая проблема: `{comment}`."
            telegram_service.send(teacher_chat_id, teacher_messange)

        edu_service.send("Error", 0, problem.max_score)
        quit()

    if str(chat_id) == "123456":
        edu_service.send("Error", 0, problem.max_score)
        quit()

    problem_variant = user_variant_resolver.get_variant(chat_id, problem)
    random_state = user_variant_resolver.get_number(chat_id, problem)
    transformer_variant = transformer_variant_strategies.get_variant_transformer_strategy_by_code(problem_variant.code)

    try:
        from student_work.solution import solution
    except Exception as e:
        comment = f"Ошибка при импортах в `{problem.name}`. Тип ошибки: {type(e)}, сообщение: {str(e)}"
        print(comment)

        for teacher_chat_id in problem.teacher_chat_id_list:
            teacher_messange = f"`{problem.name}` проверено, " \
                               + f"проект: `{pull_req_url}`, " \
                               + f"Chat ID: `{chat_id}`.\n" \
                               + f"В решении следующая проблема: `{comment}`."
            telegram_service.send(teacher_chat_id, teacher_messange)

        edu_service.send("Error", 0, problem.max_score)
        telegram_service.send(chat_id, comment)
        quit()

    try:
        test_result = solution_tester.check_solution(solution, transformer_variant, random_state)
    except Exception as e:
        comment = f"Ошибка при проверке решающей функции в `{problem.name}`. Тип ошибки: {type(e)}, сообщение: {str(e)}"
        print(comment)

        for teacher_chat_id in problem.teacher_chat_id_list:
            teacher_messange = f"`{problem.name}` проверено, " \
                               + f"проект: `{pull_req_url}`, " \
                               + f"Chat ID: `{chat_id}`, " \
                               + f"код варианта: `{problem_variant.code}`.\n" \
                               + f"В решении следующая проблема: `{comment}`."
            telegram_service.send(teacher_chat_id, teacher_messange)

        edu_service.send("Error", 0, problem.max_score)
        telegram_service.send(chat_id, comment)
        quit()

    generated_criteria_list = solution_tester.generate_criteria(transformer_variant, random_state)
    task_score, message, photo_list = result_strategy.generate(test_result, generated_criteria_list)

    edu_service.send("Done", task_score, problem.max_score)
    telegram_service.send(chat_id, message, photo_list)

    for teacher_chat_id in problem.teacher_chat_id_list:
        teacher_messange = f"`{problem.name}` проверено, " \
                           + f"проект: `{pull_req_url}`, " \
                           + f"Chat ID: `{chat_id}`, " \
                           + f"код варианта: `{problem_variant.code}`.\n" \
                           + f"Решение оценено на `{task_score}` из `{problem.max_score}`. " \
                           + f"Письмо о решении студенту..."
        telegram_service.send(teacher_chat_id, teacher_messange)
        telegram_service.send(teacher_chat_id, message, photo_list)
