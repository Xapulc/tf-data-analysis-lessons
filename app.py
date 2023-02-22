import os

from stat_problem1 import problem1, \
                          result_problem1, \
                          solution_tester_problem1_list
from tools import ProblemStorage, \
                  SolutionTesterStrategies, \
                  ResultStrategies, \
                  EduService, \
                  TelegramService, \
                  UserVariantResolver


problem_storage = ProblemStorage([
    problem1
])
solution_tester_strategies = SolutionTesterStrategies(solution_tester_problem1_list)
result_strategies = ResultStrategies([
    result_problem1
])

if __name__ == "__main__":
    task_id = os.getenv("task_id")
    problem = problem_storage.get_problem_by_task_id(task_id)
    result_strategy = result_strategies.get_result_strategy_by_code(problem.code)

    edu_service = EduService(env_file=os.getenv("GITHUB_ENV"))
    telegram_service = TelegramService(token=os.getenv("TELEGRAM_TOKEN"))
    user_variant_resolver = UserVariantResolver()

    try:
        from student_work.solution import chat_id
    except ImportError as e:
        print("Chat ID не указана")
        edu_service.send("Error", 0, problem.max_score)
        quit()

    problem_variant = user_variant_resolver.get_variant(chat_id, problem)
    random_state = user_variant_resolver.get_number(chat_id, problem)
    solution_tester = solution_tester_strategies.get_solution_tester_strategy_by_code(problem_variant.code)

    try:
        from student_work.solution import solution
    except Exception as e:
        comment = f"Ошибка при импортах. Тип ошибки: {type(e)}, сообщение: {str(e)}"
        print(comment)
        edu_service.send("Error", 0, problem.max_score)
        telegram_service.send(chat_id, comment)
        quit()

    try:
        test_result = solution_tester.check_solution(solution, random_state)
    except Exception as e:
        comment = f"Ошибка при проверке решающей функции. Тип ошибки: {type(e)}, сообщение: {str(e)}"
        print(comment)
        edu_service.send("Error", 0, problem.max_score)
        telegram_service.send(chat_id, comment)
        quit()

    task_score, message, attachment_list = result_strategy.generate(test_result)
    edu_service.send("Done", task_score, problem.max_score)
    telegram_service.send(chat_id, message, attachment_list)
