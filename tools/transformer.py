from abc import ABC, abstractmethod
from .metaclass import Singleton


class VariantTransformer(ABC):
    @abstractmethod
    def get_sample(self, iter_size, sample_size, random_state):
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
