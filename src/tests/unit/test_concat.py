from unittest import main, TestCase
from src.joiner import join_headlines, join_headlines_with_source

from src.tests.src.utils import get_headlines


class TestHeadlinesJoin(TestCase):

    def test_can_join_headlines(self):
        headlines = get_headlines(2)
        joined_headlines = join_headlines(headlines)
        expected = "Headline 0. Headline 1"
        self.assertEqual(expected, joined_headlines)

    def test_can_join_headlines_with_source(self):
        headlines = get_headlines(2)
        joined_headlines = join_headlines_with_source(headlines)
        expected = "Fonte Fonte 0: Headline 0. Fonte Fonte 1: Headline 1"
        self.assertEqual(expected, joined_headlines)


if __name__ == "__main__":
    main()
