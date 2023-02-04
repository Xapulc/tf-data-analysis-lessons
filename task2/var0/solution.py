import pandas as pd
import numpy as np

from scipy.stats import norm


def clt_solution(p: float, x: np.array) -> float:
    alpha = 1 - p
    return x.mean() - np.sqrt(np.var(x)) * norm.ppf(1 - alpha / 2) / np.sqrt(len(x)), \
           x.mean() - np.sqrt(np.var(x)) * norm.ppf(alpha / 2) / np.sqrt(len(x))


def exact_solution(p: float, x: np.array) -> float:
    alpha = 1 - p
    return x.mean() - 10 * norm.ppf(1 - alpha / 2) / np.sqrt(len(x)), \
           x.mean() - 10 * norm.ppf(alpha / 2) / np.sqrt(len(x))
