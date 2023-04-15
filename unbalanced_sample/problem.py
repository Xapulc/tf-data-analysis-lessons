from tools import Problem
from .var1 import unbalanced_sample_variant1
from .var2 import unbalanced_sample_variant2
from .var3 import unbalanced_sample_variant3


unbalanced_sample = Problem(task_id="14348",
                            code="unbalanced_sample",
                            name="Несбалансированные выборки",
                            problem_variant_list=[
                                unbalanced_sample_variant1,
                                unbalanced_sample_variant2,
                                unbalanced_sample_variant3
                            ])
