from .metaclass import Singleton
from abc import ABC, abstractmethod


class SolutionTester(ABC):
    @abstractmethod
    def check_solution(self, solution, random_state):
        pass

    @abstractmethod
    def get_code(self):
        pass


class SolutionTesterStrategies(object, metaclass=Singleton):
    def __init__(self, solution_tester_strategy_list):
        self.solution_tester_strategy_list = solution_tester_strategy_list
        self.solution_tester_strategy_by_code = {
            solution_tester_strategy.code: solution_tester_strategy
            for solution_tester_strategy in self.solution_tester_strategy_list
        }

    def get_solution_tester_strategy_by_code(self, code):
        return self.solution_tester_strategy_by_code[code]
