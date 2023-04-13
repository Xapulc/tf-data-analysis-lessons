import pandas as pd
import numpy as np

from scipy.stats import bernoulli, expon, pareto, norm, rv_discrete, beta
from tools import Problem
from .var1 import credit_card_project_variant1
from .var2 import credit_card_project_variant2
from .var3 import credit_card_project_variant3


credit_card_project = Problem(task_id="14211",
                              code="credit_card_project",
                              name="Проект по кредитным картам",
                              problem_variant_list=[
                                  credit_card_project_variant1,
                                  credit_card_project_variant2,
                                  credit_card_project_variant3
                              ])


class CreditCardProject(object):
    def __init__(self):
        self.sample_size = 123255
        self.random_state = 21
        self.mean_sale_cost = 500
        self.mean_cost = 50
        self.pareto_cc_param = 2.1
        self.pareto_service_param = 3
        self.mean_pv_cc_value = 10000
        self.mean_pv_service_value = 2000
        self.p_cc_util_scale = 0.85
        self.mean_client_income = 20000
        self.beta_parameter = 7

        min_value = 18
        max_value = 75
        value_list = np.arange(min_value, max_value + 1)

        p = 1 / value_list
        p = p / p.sum()

        self.age_dist = rv_discrete(name="age", values=(value_list, p))

        self.homo_check_metric_name = "Вероятность банкротства"

    def get_hypothesis(self, random_state):
        return True if random_state % 17 in (6, 8, 10, 14, 15, 16) else False

    def get_homo_hypothesis(self, random_state):
        return True if random_state % 13 in (5, 7, 8, 10, 12) else False

    def generate_sample(self,
                        sample_size,
                        random_state,
                        p_cc_util_scale=None,
                        mean_sale_cost=None,
                        mean_cost=None,
                        mean_client_income=None,
                        mean_pv_cc_value=None,
                        mean_pv_service_value=None,
                        beta_parameter=None):
        if p_cc_util_scale is None:
            p_cc_util_scale = self.p_cc_util_scale
        if mean_cost is None:
            mean_cost = self.mean_cost
        if mean_sale_cost is None:
            mean_sale_cost = self.mean_sale_cost
        if mean_client_income is None:
            mean_client_income = self.mean_client_income
        if mean_pv_cc_value is None:
            mean_pv_cc_value = self.mean_pv_cc_value
        if mean_pv_service_value is None:
            mean_pv_service_value = self.mean_pv_service_value
        if beta_parameter is None:
            beta_parameter = self.beta_parameter

        data = pd.DataFrame(data={
            "ID": np.arange(sample_size),
            "Возраст": self.age_dist.rvs(size=sample_size, random_state=random_state),
            "Доход клиента": pareto(3, scale=mean_client_income).rvs(size=sample_size, random_state=random_state + 1),
            "Вероятность банкротства": beta(1, beta_parameter).rvs(size=sample_size, random_state=random_state + 2)
        })

        data["Флаг утилизации счёта"] = bernoulli.rvs(p_cc_util_scale * (1 - data["Вероятность банкротства"]),
                                                      size=sample_size,
                                                      random_state=random_state + 3)

        data["Расходы"] = (expon.rvs(scale=mean_cost, size=sample_size, random_state=random_state + 4)
                           + np.where(data["Флаг утилизации счёта"] == 0, 0,
                                      expon.rvs(scale=mean_sale_cost, size=sample_size, random_state=random_state + 5))).astype(np.int64)
        data["PV КК"] = np.where(data["Флаг утилизации счёта"] == 0, 0,
                                 pareto(self.pareto_cc_param,
                                        scale=mean_pv_cc_value * (self.pareto_cc_param - 1) / self.pareto_cc_param)
                                       .rvs(size=sample_size, random_state=random_state + 6)).astype(np.int64)

        data["PV услуги"] = np.where(data["Флаг утилизации счёта"] == 0, 0,
                                     pareto(self.pareto_service_param,
                                            scale=mean_pv_service_value * (self.pareto_service_param - 1) / self.pareto_service_param)
                                           .rvs(size=sample_size, random_state=random_state + 7)).astype(np.int64)

        data["NPV"] = data["PV КК"] + data["PV услуги"] - data["Расходы"]

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
        true_homogeneity_beta = self.get_homo_hypothesis(random_state)

        beta_parameter = self.beta_parameter if true_homogeneity_beta else 6.6

        if alternative == "less":
            real_relative_mde = float(relative_mde)
        elif alternative == "greater":
            real_relative_mde = -float(relative_mde)
        else:
            if random_state % 7 in (2, 3, 5):
                real_relative_mde = float(relative_mde)
            else:
                real_relative_mde = -float(relative_mde)

        if metric_name == "Флаг утилизации счёта":
            if true_homogeneity:
                p_cc_util_scale = self.p_cc_util_scale
            else:
                p_cc_util_scale = self.p_cc_util_scale + self.p_cc_util_scale * real_relative_mde

            test_data = self.generate_sample(sample_size=sample_size,
                                             random_state=random_state + 15,
                                             p_cc_util_scale=p_cc_util_scale,
                                             beta_parameter=beta_parameter)
        elif metric_name == "PV услуги":
            if true_homogeneity:
                mean_pv_service_value = self.mean_pv_service_value
            else:
                mean_pv_service_value = self.mean_pv_service_value + self.mean_pv_service_value * real_relative_mde

            test_data = self.generate_sample(sample_size=sample_size,
                                             random_state=random_state + 41,
                                             mean_pv_service_value=mean_pv_service_value,
                                             beta_parameter=beta_parameter)
        elif metric_name == "NPV":
            rel_cc_delta = 0.1
            mean_npv = (1 - self.p_cc_util_scale) * self.mean_cost \
                       + self.p_cc_util_scale * (self.mean_pv_service_value + self.mean_pv_cc_value - self.mean_sale_cost)

            if true_homogeneity:
                mean_pv_service_value = self.mean_pv_service_value
                mean_pv_cc_value = self.mean_pv_cc_value
            else:
                delta = (mean_npv * real_relative_mde + self.p_cc_util_scale * rel_cc_delta * self.mean_pv_cc_value) \
                        / self.p_cc_util_scale
                mean_pv_service_value = self.mean_pv_service_value + delta
                mean_pv_cc_value = self.mean_pv_cc_value - rel_cc_delta * self.mean_pv_cc_value

            test_data = self.generate_sample(sample_size=sample_size,
                                             random_state=random_state + 41,
                                             mean_pv_service_value=mean_pv_service_value,
                                             mean_pv_cc_value=mean_pv_cc_value,
                                             beta_parameter=beta_parameter)

        return control_data, test_data
