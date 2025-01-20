import random


def sample(headlines: list[dict], rate: float = 0.5) -> list[dict]:
    """
    Sample elements from headlines with a rate
    """
    return random.sample(headlines, k=int(len(headlines) * rate))
