from .var1 import *
from .var2 import *
from .var3 import *
from .var4 import *
from .var5 import *
from .problem import *

result_hyp_problem2 = ResultHypProblem2(code=hyp_problem2.code,
                                        name=hyp_problem2.name,
                                        max_score=hyp_problem2.max_score)
description_generator_hyp_problem2 = DescriptionGeneratorHypProblem2(code=hyp_problem2.code,
                                                                     max_score=hyp_problem2.max_score)
solution_tester_hyp_problem2 = SolutionTesterHypProblem2(code=hyp_problem2.code,
                                                         criteria_list=hyp_problem2.criteria_list)

transformer_variant_hyp_problem2_list = [
    transformer_hyp_problem2_variant1,
    transformer_hyp_problem2_variant2,
    transformer_hyp_problem2_variant3,
    transformer_hyp_problem2_variant4,
    transformer_hyp_problem2_variant5
]
