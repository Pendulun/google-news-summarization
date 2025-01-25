from transformers import pipeline
from torch import cuda


def present_as_is(text: str) -> str:
    return text


def llm_summarization(
    text: str,
    model_name: str,
    model_kwargs: dict = None,
    pipe_kwargs: dict = None,
) -> str:
    if model_kwargs is None:
        model_kwargs = dict()

    if pipe_kwargs is None:
        pipe_kwargs = dict()

    device = "cuda" if cuda.is_available() else "cpu"
    summarizer = pipeline(
        "summarization",
        model=model_name,
        device=device,
        model_kwargs=model_kwargs,
    )

    return summarizer(text, **pipe_kwargs)[0]["summary_text"]
