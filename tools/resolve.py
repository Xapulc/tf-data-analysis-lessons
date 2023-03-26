import hashlib

from .metaclass import Singleton


class UserVariantResolver(object, metaclass=Singleton):
    def __init__(self, random_state):
        self.random_state = random_state

    def get_number(self, user, problem):
        hash_string = str(user) + problem.code + "|" + str(self.random_state)
        hash_object = hashlib.md5(hash_string.encode("utf8"))
        return int.from_bytes(hash_object.digest(), "big")

    def get_variant(self, user, problem):
        element_cnt = len(problem.problem_variant_list)
        if str(user) in ("123456", "604918251"):
            i = 2
            element_num = i % element_cnt
        else:
            hash_int = self.get_number(user, problem)
            # element_num = 1 + (hash_int % (element_cnt - 1))
            element_num = hash_int % element_cnt

        return problem.problem_variant_list[element_num]
