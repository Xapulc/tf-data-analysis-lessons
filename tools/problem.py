from .metaclass import Singleton


class Problem(object):
    def __init__(self, task_id, code, name, max_score,
                 criteria_list, problem_variant_list,
                 teacher_chat_id_list=None):
        self.task_id = task_id
        self.code = code
        self.name = name
        self.max_score = max_score
        self.criteria_list = criteria_list
        self.problem_variant_list = problem_variant_list
        self.teacher_chat_id_list = [] if teacher_chat_id_list is None \
                                    else teacher_chat_id_list


class ProblemVariant(object):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text


class ProblemStorage(object, metaclass=Singleton):
    def __init__(self, problem_list):
        self.problem_list = problem_list
        self.problem_by_task_id = {
            problem.task_id: problem
            for problem in self.problem_list
        }
        self.problem_by_code = {
            problem.code: problem
            for problem in self.problem_list
        }

    def get_problem_by_code(self, code):
        if code in self.problem_by_code.keys():
            return self.problem_by_code[code]
        else:
            raise KeyError(f"Некорректный код задания: {code}")

    def get_problem_by_task_id(self, task_id):
        if task_id in self.problem_by_task_id.keys():
            return self.problem_by_task_id[task_id]
        else:
            raise KeyError(f"Некорректный номер задания: {task_id}")
