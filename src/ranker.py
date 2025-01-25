import random


class Ranker:
    def __init__(self, entries: dict):
        self.entries = entries
        self.ranking = None

    def get_shuffled(self, seed: int = None) -> tuple[list, list]:
        random.seed(seed)
        shuffled_keys = random.sample(
            list(self.entries.keys()), k=len(self.entries)
        )
        shuffled_values = [self.entries[key] for key in shuffled_keys]
        return shuffled_keys, shuffled_values

    def define_ranking(self, presented_order: list, selected_order: list):
        """
        Return the ranking given the presented_order of the keys of entries and the
        selected order for those keys.
        Example:
        presented_order = [3, 2, 1] #Keys
        selected_order = [1, 0, 2] #Order of choice for the presented keys
        Returns {1: 2, 2: 0, 3: 1}
        """
        n_selected = len(selected_order)
        if len(presented_order) < n_selected:
            raise ValueError("You selected more than the number of options!")
        elif len(presented_order) > n_selected:
            raise ValueError(
                "You selected less than the required number of options!"
            )
        elif len(set(selected_order)) != n_selected:
            raise ValueError(
                "There are duplicated elements in the selected options!"
            )

        for el in selected_order:
            if el + 1 not in presented_order:
                raise ValueError(
                    f"The selected option {el} is not a valid option!"
                )

        return {
            presented_order[key]: id for id, key in enumerate(selected_order)
        }
