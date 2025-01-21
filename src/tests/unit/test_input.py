from unittest import main, TestCase

from sampling import sample
from tests.src.clustered_sampling_mock import ClusteredSampleMock
from tests.src.utils import get_headlines


class TestRandomSample(TestCase):

    def test_can_sample_percentage(self):
        headlines = get_headlines(10)

        sampling_rate = 0.5
        sampled_headlines = sample(headlines, rate=sampling_rate)
        self.assertTrue(len(sampled_headlines) == 5)
        for headline in sampled_headlines:
            self.assertIn(headline, headlines)

    def test_raise_when_rate_is_more_than_1(self):
        headlines = get_headlines(10)

        sampling_rate = 1.1
        with self.assertRaises(ValueError):
            _ = sample(headlines, rate=sampling_rate)

    def test_raise_when_rate_is_negative(self):
        headlines = get_headlines(10)

        sampling_rate = -0.1
        with self.assertRaises(ValueError):
            _ = sample(headlines, rate=sampling_rate)


class TestClusteredSample(TestCase):

    def test_sample_from_clusters(self):
        headlines = get_headlines(10)
        samples = ClusteredSampleMock()(headlines)
        self.assertTrue(len(samples) > 0 and len(samples) < len(headlines))
        for sample in samples:
            self.assertIn(sample, headlines)


if __name__ == "__main__":
    main()
