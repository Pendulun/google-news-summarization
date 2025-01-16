import random

def sample(headlines:list[str], rate:float=0.5) -> list[str]:
    """
    Sample elements from headlines with a rate
    """
    return random.sample(headlines, k=int(len(headlines)*rate))