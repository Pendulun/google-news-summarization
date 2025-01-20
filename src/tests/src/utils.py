def get_headlines(n: int = 10) -> list[dict]:
    """
    Returns n headlines
    """
    return [
        {"title": f"Headline {id}", "media": f"Fonte {id}"} for id in range(n)
    ]
