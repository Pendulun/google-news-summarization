import numpy as np
import torch

from src.clustered_sampling import ClusteredSample


class ClusteredSampleMock(ClusteredSample):

    @classmethod
    def get_embeddings_from_model(cls, data: list[dict]) -> np.ndarray:
        embs = np.zeros((len(data), 1))
        # Create two clusters
        embs[0 : len(data) // 2, :] += 1
        embs[len(data) // 2 :, :] += 10
        return torch.tensor(embs)
