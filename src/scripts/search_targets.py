import pathlib

import sys
from tqdm.auto import tqdm

sys.path.append("../")

from search import search

if __name__ == "__main__":
    target_searches = (
        "Cruzeiro Esporte Clube",
        "Clube Atlético Mineiro",
        "Itabirito",
        "Campeonato Mineiro de Futebol",
        "Ucrânia",
        "Donald Trump",
        "Venezuela",
        "China",
        "Rússia",
        "Síria",
        "Belo Horizonte",
        "Neymar",
        "Dólar",
        "Lula",
        "GTA 6",
    )

    data_dir_path = pathlib.Path("../../data/searches")
    file_fmt_path = "{}.csv"
    print(f"[LOG] Saving to dir {data_dir_path.resolve()}")
    pbar = tqdm(target_searches)
    for search_str in pbar:
        pbar.set_description(search_str)
        headlines = search(search_str)
        target_file_path = data_dir_path / pathlib.Path(
            file_fmt_path.format(search_str.replace(" ", "_"))
        )

        with open(target_file_path, "w") as file:
            file.write("title;link\n")
            for headline in headlines:
                file.write(
                    "{};{}\n".format(
                        headline["title"].replace(";", " "), headline["media"]
                    )
                )
