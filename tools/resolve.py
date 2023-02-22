import hashlib

from .metaclass import Singleton


class UserVariantResolver(object, metaclass=Singleton):
    def get_number(self, user, problem):
        hash_string = str(user) + problem.code
        hash_object = hashlib.md5(hash_string.encode("utf8"))
        return int.from_bytes(hash_object.digest(), "big")

    def get_variant(self, user, problem):
        if str(user) in ("123456", "604918251"):
            return problem.problem_variant_list[1]
        else:
            hash_int = self.get_number(user, problem)
            element_cnt = len(problem.problem_variant_list)
            element_num = hash_int % element_cnt
            return problem.problem_variant_list[element_num]
