import argparse
import pathlib
import pandas as pd
import sys

sys.path.append("..")

from ranker import Ranker


def config_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--summaries_path",
        required=True,
        type=str,
        help="The path to the csv file with summaries results for every searched term.",
    )

    parser.add_argument(
        "--save_to",
        required=True,
        type=str,
        help="The csv file path to where save the rankings.",
    )

    return parser


if __name__ == "__main__":
    args = config_parser().parse_args()

    summaries_df = pd.read_csv(
        pathlib.Path(args.summaries_path), delimiter=";", index_col="Unnamed: 0"
    )

    ranking_results = dict()
    n_of_terms = len(summaries_df)
    for idx, (row_index, row) in enumerate(summaries_df.iterrows()):
        ranker = Ranker(row.to_dict())
        shuffled_keys, shuffled_texts = ranker.get_shuffled()

        should_present_question = True
        while should_present_question:
            print("\n")
            print(f"({idx+1}/{n_of_terms}) TERM: {row_index}")
            print("\n")
            for id, text in enumerate(shuffled_texts):
                print(id, " - ", text)
                print("\n")

            user_input = input("Order of preference: ").strip().split()
            try:
                user_input = [int(el) for el in user_input]
                summaries_rankings = ranker.define_ranking(
                    [int(el) for el in shuffled_keys], user_input
                )
            except Exception as e:
                print("\n\n\n\n\n\n")
                print("TRY AGAIN!", str(e))
            else:
                should_present_question = False
                ranking_results[row_index] = summaries_rankings

    print("[LOG] Saving results to", args.save_to)
    pd.DataFrame(ranking_results).sort_index().to_csv(
        pathlib.Path(args.save_to)
    )
