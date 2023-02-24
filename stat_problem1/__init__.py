from .var0 import *
from .var1 import *
from .problem import *

result_problem1 = ResultProblem1(code=problem1.code,
                                 name=problem1.name,
                                 max_score=problem1.max_score)
description_generator_problem1 = DescriptionGeneratorProblem1(code=problem1.code,
                                                              max_score=problem1.max_score)
solution_tester_problem1 = SolutionTesterProblem1(code=problem1.code)

transformer_variant_problem1_list = [
    transformer_problem1_variant0,
    transformer_problem1_variant1
]
