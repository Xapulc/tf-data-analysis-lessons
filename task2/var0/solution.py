import numpy as np

from scipy.stats import norm


def solution(p: float, x: np.array):
    alpha = 1 - p
    return x.mean() - np.sqrt(np.var(x)) * norm.ppf(1 - alpha / 2) / np.sqrt(len(x)), \
           x.mean() - np.sqrt(np.var(x)) * norm.ppf(alpha / 2) / np.sqrt(len(x))
