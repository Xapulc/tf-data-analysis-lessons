from abc import ABC, abstractmethod
from .metaclass import Singleton


class VariantTransformer(ABC):
    @abstractmethod
    def _get_default_sample(self):
        pass

    @abstractmethod
    def get_sample(self, random_state):
        pass

    @abstractmethod
    def get_score_list(self, random_state):
        pass

    @abstractmethod
    def get_description(self, random_state):
        pass


class VariantTransformerStrategies(object, metaclass=Singleton):
    def __init__(self, variant_transformer_strategy_list):
        self.variant_transformer_strategy_list = variant_transformer_strategy_list
        self.variant_transformer_strategy_by_code = {
            variant_transformer_strategy.code: variant_transformer_strategy
            for variant_transformer_strategy in self.variant_transformer_strategy_list
        }

    def get_variant_transformer_strategy_by_code(self, code):
        return self.variant_transformer_strategy_by_code[code]
