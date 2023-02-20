import hashlib

from abc import ABC, abstractmethod, property


class Problem(ABC):
    def __init__(self):
        pass
    
    @property
    @abstractmethod
    def code(self):
        pass
    
    @property
    @abstractmethod
    def name(self):
        pass
    
    @property
    @abstractmethod
    def max_score(self):
        pass
    
    @property
    @abstractmethod
    def problem_variant_list(self):
        pass
    
    @abstractmethod
    def make_notification(self, task_score, test_result):
        pass
        
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
    
    def make_test(self, solution, user):
        user = str(user)
        problem_variant = self._get_problem_variant(user)
        task_score, comment, test_result = problem_variant.make_test(solution, self._get_random_user_number(user))
        self.make_notification(task_score, test_result)
        return task_score, comment
