from .metaclass import Singleton
from abc import ABC, abstractmethod


class DescriptionGenerator(ABC):
    @abstractmethod
    def get_description(self, transformer_variant, random_state):
        pass

    @abstractmethod
    def _get_estimation_text(self, transformer_variant, random_state):
        pass

    @abstractmethod
    def get_code(self):
        pass


class DescriptionGeneratorStrategies(object, metaclass=Singleton):
    def __init__(self, description_generator_strategy_list):
        self.description_generator_strategy_list = description_generator_strategy_list
        self.description_generator_strategy_by_code = {
            description_generator_strategy.code: description_generator_strategy
            for description_generator_strategy in self.description_generator_strategy_list
        }

    def get_description_generator_strategy_by_code(self, code):
        return self.description_generator_strategy_by_code[code]
