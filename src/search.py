from GoogleNews import GoogleNews


def search(search_str: str) -> list[dict]:
    """
    Search the search_str on google news. Returns a list of dicts
    with the news title and link.
    """
    googlenews = GoogleNews(lang="pt", region="BR", period="1d", encode="utf-8")
    googlenews.enableException(True)
    googlenews.clear()
    googlenews.get_news(search_str)
    results = [
        {"title": result["title"], "media": result["media"]}
        for result in googlenews.results()
    ]
    return results
