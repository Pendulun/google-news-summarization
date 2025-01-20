def join_headlines(headlines: list[dict]) -> str:
    return ". ".join([headline["title"] for headline in headlines]).strip()


def join_headlines_with_source(headlines: list[dict]) -> str:
    texts = [
        "Fonte {}: {}".format(headline["media"], headline["title"])
        for headline in headlines
    ]
    return ". ".join(texts).strip()
