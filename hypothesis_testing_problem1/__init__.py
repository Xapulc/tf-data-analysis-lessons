from .var0 import *
from .var1 import *
from .problem import *

result_hyp_problem1 = ResultHypProblem1(code=hyp_problem1.code,
                                        name=hyp_problem1.name,
                                        max_score=hyp_problem1.max_score)
description_generator_hyp_problem1 = DescriptionGeneratorHypProblem1(code=hyp_problem1.code,
                                                                     max_score=hyp_problem1.max_score)
solution_tester_hyp_problem1 = SolutionTesterHypProblem1(code=hyp_problem1.code,
                                                         criteria_list=hyp_problem1.criteria_list)

transformer_variant_hyp_problem1_list = [
    transformer_hyp_problem1_variant0,
    transformer_hyp_problem1_variant1
]
