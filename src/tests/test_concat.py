from unittest import main, TestCase
from joiner import join_headlines, join_headlines_with_source


class TestHeadlinesJoin(TestCase):
    def _get_headlines_info(self, n: int = 10) -> list[dict]:
        """
        Returns n headlines
        """
        return [
            {"title": f"Headline {id}", "media": f"{id}"} for id in range(n)
        ]

    def test_can_join_headlines(self):
        headlines = self._get_headlines_info(2)
        joined_headlines = join_headlines(headlines)
        expected = "Headline 0. Headline 1"
        self.assertEqual(expected, joined_headlines)

    def test_can_join_headlines_with_source(self):
        headlines = self._get_headlines_info(2)
        joined_headlines = join_headlines_with_source(headlines)
        expected = "Fonte 0: Headline 0. Fonte 1: Headline 1"
        self.assertEqual(expected, joined_headlines)


if __name__ == "__main__":
    main()
