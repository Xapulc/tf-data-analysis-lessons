import pandas as pd
import numpy as np

from scipy.stats import bernoulli, expon, pareto, norm
from tools import Problem
from .var1 import telesales_project_variant1
from .var2 import telesales_project_variant2
from .var3 import telesales_project_variant3


telesales_project = Problem(task_id="14138",
                            code="telesales_project",
                            name="Проект по обзвонам",
                            problem_variant_list=[
                                telesales_project_variant1,
                                telesales_project_variant2,
                                telesales_project_variant3
                            ])


class TelesalesProject(object):
    def __init__(self):
        self.sample_size = 72161
        self.random_state = 42
        self.p_call = 0.6
        self.p_sale = 0.5
        self.mean_sale_cost = 500
        self.mean_cost = 50
        self.pareto_param = 4
        self.mean_pv_value = 1600

    def get_hypothesis(self, random_state):
        return True if random_state % 14 in (3, 5, 8, 9, 10) else False

    def generate_sample(self,
                        sample_size,
                        random_state,
                        p_call=None,
                        p_sale=None,
                        mean_sale_cost=None,
                        mean_cost=None,
                        mean_pv_value=None):
        if p_call is None:
            p_call = self.p_call
        if p_sale is None:
            p_sale = self.p_sale
        if mean_cost is None:
            mean_cost = self.mean_cost
        if mean_sale_cost is None:
            mean_sale_cost = self.mean_sale_cost
        if mean_pv_value is None:
            mean_pv_value = self.mean_pv_value

        data = pd.DataFrame(data={
            "ID": np.arange(sample_size),
            "Флаг дозвона": bernoulli.rvs(p_call, size=sample_size, random_state=random_state)
        })

        data["Флаг продажи"] = np.where(data["Флаг дозвона"] == 0, 0,
                                        bernoulli.rvs(p_sale, size=sample_size, random_state=random_state + 1))

        data["Расходы"] = expon.rvs(scale=mean_cost, size=sample_size, random_state=random_state + 2) \
                          + np.where(data["Флаг продажи"] == 0, 0,
                                     expon.rvs(scale=mean_sale_cost, size=sample_size, random_state=random_state + 3))
        data["PV"] = np.where(data["Флаг продажи"] == 0, 0,
                              pareto(self.pareto_param, scale=mean_pv_value * (self.pareto_param - 1) / self.pareto_param).rvs(size=sample_size, random_state=random_state + 4))

        data["Расходы"] = data["Расходы"].astype(np.int64)
        data["PV"] = data["PV"].astype(np.int64)
        data["NPV"] = data["PV"] - data["Расходы"]

        return data

    def get_sample_size(self, metric_name, alternative, alpha, beta, relative_mde, gamma=0.5):
        data = self.generate_sample(sample_size=self.sample_size,
                                    random_state=self.random_state)
        sigma_sqr = data[metric_name].var()
        mde = data[metric_name].mean() * float(relative_mde)
        alpha_ = float(alpha) / 2 if alternative == "two-sided" else float(alpha)
        factor = sigma_sqr * ((norm.ppf(1 - alpha_) - norm.ppf(float(beta)))**2) / (mde**2)

        return factor / (1 - float(gamma)), factor / float(gamma)

    def generate_test_sample(self, sample_size, metric_name, alternative, relative_mde, random_state):
        control_data = self.generate_sample(sample_size=sample_size,
                                            random_state=random_state)

        true_homogeneity = self.get_hypothesis(random_state)

        if alternative == "less":
            real_relative_mde = float(relative_mde)
        elif alternative == "greater":
            real_relative_mde = -float(relative_mde)
        else:
            if random_state % 3 == 1:
                real_relative_mde = float(relative_mde)
            else:
                real_relative_mde = -float(relative_mde)

        if metric_name == "NPV":
            npv_mean = self.p_call * self.p_sale * (self.mean_pv_value - self.mean_sale_cost) - self.mean_cost
            if true_homogeneity:
                mean_pv_value = self.mean_pv_value
            else:
                mean_pv_value = self.mean_pv_value + npv_mean * real_relative_mde / (self.p_call * self.p_sale)

            test_data = self.generate_sample(sample_size=sample_size,
                                             random_state=random_state+1,
                                             mean_pv_value=mean_pv_value)
        elif metric_name == "Флаг продажи":
            if true_homogeneity:
                p_sale = self.p_sale
            else:
                p_sale = self.p_sale + self.p_sale * real_relative_mde

            test_data = self.generate_sample(sample_size=sample_size,
                                             random_state=random_state+1,
                                             p_sale=p_sale)
        elif metric_name == "Расходы":
            mean_sale_cost_per_task = self.mean_sale_cost * self.p_call * self.p_sale
            if true_homogeneity:
                mean_sale_cost = self.mean_sale_cost
            else:
                mean_sale_cost = self.mean_sale_cost \
                                 + self.mean_sale_cost * real_relative_mde \
                                   * (self.mean_cost + mean_sale_cost_per_task) / mean_sale_cost_per_task

            test_data = self.generate_sample(sample_size=sample_size,
                                             random_state=random_state+1,
                                             mean_sale_cost=mean_sale_cost)

        return control_data, test_data
