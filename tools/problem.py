class Problem(object):
    def __init__(self, code, name, max_score, problem_variant_list):
        self.code = code
        self.name = name
        self.max_score = max_score
        self.problem_variant_list = problem_variant_list
        
        
class ProblemVariant(object):
    def __init__(self, template):
        self.template = template
        
        
class GeneratedProblemVariant(object):
    def __init__(self, random_state, description):
        self.random_state = random_state
        self.description = description
