from .var0 import *
from .var1 import *
from .problem import *

result_problem1 = ResultProblem1(code=problem1.code,
                                 name=problem1.name,
                                 max_score=problem1.max_score)
solution_tester_problem1_list = [
    solution_tester_problem1_variant0,
    solution_tester_problem1_variant1
]
description_generator_problem1_list = [
    description_generator_problem1_variant0,
    description_generator_problem1_variant1
]
