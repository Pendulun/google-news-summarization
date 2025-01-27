import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pathlib

cols_ordering = [
    "Síria",
    "Rússia",
    "China",
    "Ucrânia",
    "Venezuela",
    "Belo_Horizonte",
    "Itabirito",
    "Lula",
    "Donald_Trump",
    "Neymar",
    "Campeonato_Mineiro_de_Futebol",
    "Cruzeiro_Esporte_Clube",
    "Clube_Atlético_Mineiro",
    "Dólar",
    "GTA_6",
]

index_to_meaning = {
    1: "Random",
    2: "Random_Summ",
    3: "Cluster_Source",
    4: "Cluster_Source_Summ",
    5: "Source_Summ",
}


def plot_each_person_results(data_dir: str, save_to_dir: str):
    target_dir_path = pathlib.Path(save_to_dir)
    target_dir_path.mkdir(exist_ok=True, parents=True)

    data_dir_path = pathlib.Path(data_dir)
    for file in data_dir_path.glob("*.csv"):
        df = pd.read_csv(file, index_col="Unnamed: 0")
        df = df[cols_ordering]
        df.index = df.index.map(index_to_meaning)

        plt.figure(figsize=(12, 5))
        df.T.plot(ax=plt.gca(), marker="o")

        x_labels = df.columns.to_list()
        plt.xticks(range(len(x_labels)), x_labels, rotation=40)
        y_ticks = [0, 1, 2, 3, 4]
        plt.yticks(y_ticks, [el + 1 for el in y_ticks])
        plt.ylim((-1, len(y_ticks)))
        plt.ylabel("Ranking")
        plt.gca().invert_yaxis()

        plt.legend(loc="upper left", ncol=len(plt.gca().lines))
        plt.title(file.stem)
        plt.tight_layout()

        plt.savefig(target_dir_path / f"{file.stem}.png")
        plt.close()


def get_configs_mean_rankings(data_dir: str) -> dict[dict[str, float]]:
    data_dir_path = pathlib.Path(data_dir)
    config_term_rankings = dict()
    for file_path in data_dir_path.glob("*.csv"):
        df = pd.read_csv(file_path, index_col="Unnamed: 0")
        df.index = df.index.map(index_to_meaning)

        for config_id, row in df.iterrows():
            row_data = row.to_dict()
            for term, ranking in row_data.items():
                config_term_rankings.setdefault(config_id, dict()).setdefault(
                    term, list()
                ).append(ranking)

    config_term_mean_rankings = dict()
    for config_id, terms_rankings in config_term_rankings.items():
        for term, rankings in terms_rankings.items():
            mean_ranking = np.array(rankings).mean()
            config_term_mean_rankings.setdefault(config_id, dict())[term] = (
                mean_ranking.item() + 1
            )

    return config_term_mean_rankings


def save_mean_rankings_plot(data_dir: str, target_plot_path: str):
    data_dir_path = pathlib.Path(data_dir)

    config_term_mean_rankings = get_configs_mean_rankings(data_dir_path)

    mean_rankings_df = pd.DataFrame(config_term_mean_rankings)
    mean_rankings_df = mean_rankings_df.loc[cols_ordering]

    plt.figure(figsize=(12, 5))
    mean_rankings_df.plot(ax=plt.gca(), marker="o")

    x_labels = mean_rankings_df.index.to_list()
    plt.xticks(range(len(x_labels)), x_labels, rotation=40)

    y_ticks = [1, 2, 3, 4, 5]
    plt.yticks(y_ticks, [el for el in y_ticks])
    plt.ylim((0, len(y_ticks) + 1))

    plt.ylabel("Mean Ranking")
    plt.gca().invert_yaxis()

    plt.legend(loc="upper left", ncol=len(plt.gca().lines))
    plt.title("Configs mean rankings per term")
    plt.tight_layout()

    plt.savefig(pathlib.Path(target_plot_path))
    plt.close()


if __name__ == "__main__":
    data_dir = pathlib.Path("../../data")
    rankings_data_dir = data_dir / "rankings"

    target_plots_dir = data_dir / "assets/rankings/"
    print("[LOG] Plotting each person results to", target_plots_dir.resolve())
    plot_each_person_results(rankings_data_dir, target_plots_dir)

    mean_rankings_plot_path = data_dir / "assets/rankings/mean_rankings.png"
    print("[LOG] Plotting mean rankings to", mean_rankings_plot_path.resolve())
    save_mean_rankings_plot(rankings_data_dir, mean_rankings_plot_path)
