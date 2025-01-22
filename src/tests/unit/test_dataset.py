import numpy as np
from unittest import main, TestCase

from src.clustered_sampling import HeadlinesDataset
from src.tests.src.utils import get_headlines


class TestHeadlinesDataset(TestCase):

    def test_can_get_len(self):
        headlines = get_headlines(4)
        self.assertTrue(len(HeadlinesDataset(headlines)) == 4)

    def test_can_get_one_element(self):
        headlines = get_headlines(4)
        dataset = HeadlinesDataset(headlines)

        target_headline_idx = 2
        expected = headlines[target_headline_idx]
        returned = dataset[target_headline_idx]
        self.assertDictEqual(returned, expected)

    def test_can_get_3_elements(self):
        headlines = get_headlines(4)
        dataset = HeadlinesDataset(headlines)

        target_headline_idxs = [1, 2, 3]
        expected = np.array([headlines[idx] for idx in target_headline_idxs])
        returned = dataset[target_headline_idxs]
        self.assertTrue(np.all(returned == expected))


if __name__ == "__main__":
    main()
