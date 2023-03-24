from .var1 import *
from .var2 import *
from .problem import *

result_hyp_problem3 = ResultHypProblem3(code=hyp_problem3.code,
                                        name=hyp_problem3.name,
                                        max_score=hyp_problem3.max_score)
description_generator_hyp_problem3 = DescriptionGeneratorHypProblem3(code=hyp_problem3.code,
                                                                     max_score=hyp_problem3.max_score)
solution_tester_hyp_problem3 = SolutionTesterHypProblem3(code=hyp_problem3.code,
                                                         criteria_list=hyp_problem3.criteria_list)

transformer_variant_hyp_problem3_list = [
    transformer_hyp_problem3_variant1,
    transformer_hyp_problem3_variant2
]
