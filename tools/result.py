from .metaclass import Singleton
from abc import ABC, abstractmethod


class Result(ABC):
    @abstractmethod
    def generate(self, test_result, generated_criteria_list):
        pass

    @abstractmethod
    def get_code(self):
        pass


class ResultStrategies(object, metaclass=Singleton):
    def __init__(self, result_strategy_list):
        self.result_strategy_list = result_strategy_list
        self.result_strategy_by_code = {
            result_strategy.code: result_strategy
            for result_strategy in self.result_strategy_list
        }

    def get_result_strategy_by_code(self, code):
        return self.result_strategy_by_code[code]
