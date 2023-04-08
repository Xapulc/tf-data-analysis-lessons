from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description="Преобразователь ссылки студента")
    parser.add_argument("github_url")

    args = parser.parse_args()
    print(args.github_url)
