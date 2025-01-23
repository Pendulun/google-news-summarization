import argparse
import pathlib

from src.pipeline import PipelineBuilder, JoinerTypes, SamplerTypes, SolverTypes
from src.search import search


def config_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--search",
        type=str,
        required=False,
        default=None,
        help="What to search for in Google News",
    )

    parser.add_argument(
        "--data_path",
        type=str,
        required=False,
        default=None,
        help="The path to a csv file with two columns ('title' and 'media') to proccess",
    )

    return parser


def search_and_summarize(
    search_str: str,
    sampler_type: SamplerTypes,
    joiner_type: JoinerTypes,
    solver_type: SolverTypes,
    sampler_kwargs: dict = None,
    joiner_kwargs: dict = None,
    solver_kwargs: dict = None,
) -> str:
    """
    Searches a term and them summarize it
    """
    print(f"[LOG] Searching for term: {search_str}")
    results = search(search_str)

    print(f"[LOG] Summarizing")
    return summarize(
        results,
        sampler_type,
        joiner_type,
        solver_type,
        sampler_kwargs,
        joiner_kwargs,
        solver_kwargs,
    )


def load_and_summarize(
    data_path: str,
    sampler_type: SamplerTypes,
    joiner_type: JoinerTypes,
    solver_type: SolverTypes,
    sampler_kwargs: dict = None,
    joiner_kwargs: dict = None,
    solver_kwargs: dict = None,
) -> str:
    """
    Load the headlines from a file and them sumarize them
    """
    headlines = list()
    data_path = pathlib.Path(data_path)
    print(f" [LOG] Reading {data_path.resolve()}")
    with open(data_path, "r") as file:
        for idx, line in enumerate(file):
            # Jump header
            if idx == 0:
                continue

            title, media = line.split(";")
            headline = {
                "title": title.strip().strip("\n"),
                "media": media.strip().strip("\n"),
            }
            headlines.append(headline)

    print(f"[LOG] Summarizing")
    return summarize(
        headlines,
        sampler_type,
        joiner_type,
        solver_type,
        sampler_kwargs,
        joiner_kwargs,
        solver_kwargs,
    )


def summarize(
    headlines: list[dict],
    sampler_type: SamplerTypes,
    joiner_type: JoinerTypes,
    solver_type: SolverTypes,
    sampler_kwargs: dict = None,
    joiner_kwargs: dict = None,
    solver_kwargs: dict = None,
) -> str:
    pipe = PipelineBuilder.build(sampler_type, joiner_type, solver_type)
    return pipe.run(headlines, sampler_kwargs, joiner_kwargs, solver_kwargs)


if __name__ == "__main__":
    args = config_argparser().parse_args()

    sampler = SamplerTypes.RANDOM
    joiner = JoinerTypes.WITH_SOURCE
    solver = SolverTypes.AS_IS

    if args.search is not None:
        print(search_and_summarize(args.search, sampler, joiner, solver))
    elif args.data_path is not None:
        print(load_and_summarize(args.data_path, sampler, joiner, solver))
    else:
        raise ValueError(
            "One should give a search term or a data_path where to load headlines from!"
        )
