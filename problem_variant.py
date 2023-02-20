from abc import ABC, abstractmethod, property

class ProblemVariant(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_description(random_state):
        pass
    
    @abstractmethod
    def make_test(solution, random_state):
        pass
