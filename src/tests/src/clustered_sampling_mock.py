import numpy as np
from torch.utils.data import Dataset

from clustered_sampling import ClusteredSample


class ClusteredSampleMock(ClusteredSample):
    @classmethod
    def set_model(cls, model_name: str):
        pass

    @classmethod
    def get_embeddings(cls, dataset: Dataset, batch_size: int) -> np.ndarray:
        embs = np.zeros((len(dataset), 1))
        # Create two clusters
        embs[0 : len(dataset) // 2, :] += 1
        embs[len(dataset) // 2 :, :] += 10
        return embs
