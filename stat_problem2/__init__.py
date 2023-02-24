from .var0 import *
from .problem import *

result_problem2 = ResultProblem2(code=problem2.code,
                                 name=problem2.name,
                                 max_score=problem2.max_score)
description_generator_problem2 = DescriptionGeneratorProblem2(code=problem2.code,
                                                              max_score=problem2.max_score)
solution_tester_problem2 = SolutionTesterProblem2(code=problem2.code)

transformer_variant_problem2_list = [
    transformer_problem2_variant0
]
