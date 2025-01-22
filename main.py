import argparse
from GoogleNews import GoogleNews

from src.pipeline import PipelineBuilder, JoinerTypes, SamplerTypes, SolverTypes


def config_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--search",
        type=str,
        required=True,
        help="What to search for in Google News",
    )
    return parser


def search(search_str: str) -> list[dict]:
    googlenews = GoogleNews(lang="pt", region="BR", period="1d", encode="utf-8")
    print("Google News API version:", googlenews.getVersion())
    googlenews.enableException(True)
    googlenews.clear()
    googlenews.get_news(search_str)
    results = [
        {"title": result["title"], "media": result["media"]}
        for result in googlenews.results()
    ]
    return results


def summarize(
    search_str: str,
    sampler_type: SamplerTypes,
    joiner_type: JoinerTypes,
    solver_type: SolverTypes,
    sampler_kwargs: dict = None,
    joiner_kwargs: dict = None,
    solver_kwargs: dict = None,
) -> str:
    results = search(search_str)
    pipe = PipelineBuilder.build(sampler_type, joiner_type, solver_type)
    return pipe.run(results, sampler_kwargs, joiner_kwargs, solver_kwargs)


if __name__ == "__main__":
    args = config_argparser().parse_args()

    sampler = SamplerTypes.RANDOM
    joiner = JoinerTypes.WITH_SOURCE
    solver = SolverTypes.AS_IS

    print(summarize(args.search, sampler, joiner, solver))
