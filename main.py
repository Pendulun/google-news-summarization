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


if __name__ == "__main__":
    args = config_argparser().parse_args()
    results = search(args.search)

    sampler = SamplerTypes.RANDOM
    joiner = JoinerTypes.WITH_SOURCE
    solver = SolverTypes.AS_IS
    pipe = PipelineBuilder.build(sampler, joiner, solver)

    print(pipe.run(results))
