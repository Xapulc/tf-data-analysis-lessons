from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description="Преобразователь ссылки студента")
    parser.add_argument("github_url")

    args = parser.parse_args()
    github_url = args.github_url
    if "/blob/" not in github_url:
        print(github_url)
    else:
        print(github_url[:github_url.rfind("/blob")])
