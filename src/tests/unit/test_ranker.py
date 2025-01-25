from unittest import TestCase, main
from src.ranker import Ranker


class TestRanker(TestCase):
    def _get_entry(self) -> dict[int, str]:
        return {1: "a", 2: "b", 3: "c"}

    def test_can_shuffle_entry(self):
        entry = self._get_entry()
        ranker = Ranker(entry)
        _, values = ranker.get_shuffled()
        self.assertNotEqual(entry.values(), values)
        for el in values:
            self.assertIn(el, entry.values())

    def test_can_define_rank(self):
        entry = self._get_entry()
        ranker = Ranker(entry)
        presented_order = [3, 2, 1]
        selected_order = [1, 0, 2]
        expected_ranking = {1: 2, 2: 0, 3: 1}
        self.assertEqual(
            ranker.define_ranking(presented_order, selected_order),
            expected_ranking,
        )

    def test_raises_if_ranking_has_duplicated_elements(self):
        entry = self._get_entry()
        ranker = Ranker(entry)
        presented_order = [3, 2, 1]
        selected_order = [1, 2, 2]
        with self.assertRaises(ValueError):
            ranker.define_ranking(presented_order, selected_order)

    def test_raises_if_ranking_has_less_elements_than_necessary(self):
        entry = self._get_entry()
        ranker = Ranker(entry)
        presented_order = [3, 2, 1]
        selected_order = [1, 2]
        with self.assertRaises(ValueError):
            ranker.define_ranking(presented_order, selected_order)

    def test_raises_if_ranking_has_more_elements_than_necessary(self):
        entry = self._get_entry()
        ranker = Ranker(entry)
        presented_order = [3, 2, 1]
        selected_order = [1, 2, 3, 4]
        with self.assertRaises(ValueError):
            ranker.define_ranking(presented_order, selected_order)

    def test_raises_if_has_elements_not_present_in_presented_order(self):
        entry = self._get_entry()
        ranker = Ranker(entry)
        presented_order = [3, 2, 1]
        selected_order = [1, 4, 3]
        with self.assertRaises(ValueError):
            ranker.define_ranking(presented_order, selected_order)


if __name__ == "__main__":
    main()
