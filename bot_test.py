from tools import Converter


if __name__ == "__main__":
    text = """
    \\section{Входные данные}
    Одномерный массив numpy.ndarray
    длин прыжков (в сантиметрах) одного спортсмена.
    """
    converter = Converter()
    print(converter.convert_tex_body_str_to_image_list(text))
