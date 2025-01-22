from unittest import main, TestCase
from src.solvers import present_as_is


class TestSolvers(TestCase):
    def test_just_replicate(self):
        text = "Fonte 1: Headline 1. Fonte 2: Headline 2"
        replicated_text = present_as_is(text)
        self.assertEqual(text, replicated_text)


if __name__ == "__main__":
    main()
