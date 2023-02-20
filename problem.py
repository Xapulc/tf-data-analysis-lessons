import abc
import hashlib


class Problem(metaclass=abc.ABCMeta):
    def __init__(self, code, name, max_score, problem_variant_list):
        self.code = code
        self.name = name
        self.max_score = max_score
        self.problem_variant_list = problem_variant_list
        
    def _get_random_user_number(self, user: str):
        hash_string = user + self.name
        hash_object = hashlib.md5(hash_string.encode("utf8"))
        hash_int = int.from_bytes(hash_object.digest(), "big")
        return hash_int
        
    def _get_problem_variant(self, user: str):
        variant_cnt = len(self.problem_variant_list)
        hash_int = self._get_random_user_number(user)
        variant = hash_int % variant_cnt
        return problem_variant_list[variant]
        
    def get_description(self, user):
        user = str(user)
        problem_variant = self._get_problem_variant(user)
        return problem_variant.get_description(self._get_random_user_number(user))
    
    @abc.abstractmethod
    def make_notification(self, task_score, test_result):
        pass
    
    def make_test(self, solution, user):
        user = str(user)
        problem_variant = self._get_problem_variant(user)
        task_score, comment, test_result = problem_variant.make_test(solution, self._get_random_user_number(user))
        self.make_notification(task_score, test_result)
        return task_score, comment
