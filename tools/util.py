import numpy as np
import re

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR


def round_up(x, decimals=0):
    dec_x = Decimal(x)
    target_dec = Decimal("1." + (int(decimals) * "0"))
    return dec_x.quantize(target_dec, ROUND_CEILING)


def round_down(x, decimals=0):
    dec_x = Decimal(x)
    target_dec = Decimal("1." + (int(decimals) * "0"))
    return dec_x.quantize(target_dec, ROUND_FLOOR)


def first_decimal(x):
    return -np.ceil(-np.log10(x))


def round_up_first_decimal(x, decimals=0):
    if x > 0:
        x_decimal = -first_decimal(x)
        return round_up(x, x_decimal + decimals)
    else:
        return 0


def round_down_first_decimal(x, decimals=0):
    if x > 0:
        x_decimal = -first_decimal(x)
        return round_down(x, x_decimal + decimals)
    else:
        return 0


def find_chat_id(file_name):
    chat_id = None
    with open(file_name, "r") as solution_file:
        for line in solution_file.readlines():
            if "chat_id" in line:
                int_list = re.findall(r"\d+", line)
                if len(int_list) > 0:
                    chat_id = int(int_list[0])

    return chat_id
