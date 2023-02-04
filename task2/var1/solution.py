import pandas as pd
import numpy as np

from scipy.stats import norm, gamma


def clt_solution_with_unknown_variance(p: float, x: np.array) -> float:
    alpha = 1 - p
    return x.mean() / 50 + 1 / 100 - np.sqrt(np.var(x)) * norm.ppf(1 - alpha / 2) / (50 * np.sqrt(len(x))), \
           x.mean() / 50 + 1 / 100 - np.sqrt(np.var(x)) * norm.ppf(alpha / 2) / (50 * np.sqrt(len(x)))


def clt_solution_with_known_variance(p: float, x: np.array) -> float:
    alpha = 1 - p
    return x.mean() / 50 + 1 / 100 - norm.ppf(1 - alpha / 2) / (50 * np.sqrt(len(x))), \
           x.mean() / 50 + 1 / 100 - norm.ppf(alpha / 2) / (50 * np.sqrt(len(x)))


def exact_solution(p: float, x: np.array) -> float:
    alpha = 1 - p
    return gamma.ppf(alpha / 2, len(x), loc=x.mean() / 50 - 1 / 100, scale=1 / (50 * len(x))), \
           gamma.ppf(1 - alpha / 2, len(x), loc=x.mean() / 50 - 1 / 100, scale=1 / (50 * len(x)))
