import random

import numpy as np
from sklearn.cluster import DBSCAN
import torch
from torch.utils.data import Dataset, DataLoader
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModel


class HeadlinesDataset(Dataset):
    def __init__(self, headlines: list[dict]):
        self.headlines = np.array(headlines)

    def __len__(self):
        return len(self.headlines)

    def __getitem__(self, idx) -> list[dict[str, str]]:
        return self.headlines[idx]


class ClusteredSample:
    model = None
    tokenizer = None
    device = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    def set_model(cls, model_name: str):
        cls.tokenizer = AutoTokenizer.from_pretrained(model_name)
        cls.model = AutoModel.from_pretrained(model_name).to(cls.device)

    def __call__(
        self,
        headlines: list[dict],
        model_name: str,
        batch_size: int = 32,
        cluster_kwargs: dict = None,
    ) -> list[dict]:
        """
        Clusters the headlines titles and sample one per cluster
        """
        if cluster_kwargs is None:
            cluster_kwargs = {"eps": 0.3, "min_samples": 2}
        self.set_model(model_name)
        dataset = HeadlinesDataset(headlines)
        np_embs = self.get_embeddings(dataset, batch_size)
        cluster_labels = self._get_clustering_labels(np_embs, cluster_kwargs)
        sampled = list()
        for label in np.unique(cluster_labels):
            representative = self._get_most_representative_member(
                dataset, np_embs, cluster_labels, label
            )
            sampled.append(representative)
        return sampled

    def _get_most_representative_member(
        self,
        dataset: HeadlinesDataset,
        np_embs: np.ndarray,
        cluster_labels: np.ndarray,
        label: int,
    ):
        """
        Return the cluster label member with the closest embedding
         to the mean embedding
        """
        cluster_data = dataset[np.where(cluster_labels == label)]
        cluster_embs = np_embs[np.where(cluster_labels == label)]
        mean_emb = cluster_embs.mean(axis=0)
        distances = np.linalg.norm(cluster_embs - mean_emb, axis=1)
        representative = cluster_data[np.argsort(distances)[0]]
        return representative

    def _get_clustering_labels(
        self, data: np.ndarray, cluster_kwargs: dict
    ) -> np.ndarray:
        clustering = DBSCAN(n_jobs=-1, **cluster_kwargs).fit(data)
        return clustering.labels_

    @classmethod
    def get_embeddings(cls, dataset, batch_size: int = 16) -> np.ndarray:
        """
        Returns the embeddings for the dataset
        """
        embeddings = list()
        for i, batch in tqdm(
            enumerate(
                DataLoader(
                    dataset, batch_size=batch_size, collate_fn=lambda x: x
                )
            ),
            desc="Calc embeddings",
        ):
            embs = cls.get_embeddings_from_model(batch)
            embeddings.append(embs)

        np_embs = torch.cat(embeddings).numpy()
        return np_embs

    @classmethod
    def get_embeddings_from_model(cls, data: list[dict]):
        """
        Uses the class tokenizer and model to calculate the data
        embeddings
        """
        encoded_data = cls.tokenizer(
            [el["title"] for el in data],
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(cls.device)
        with torch.autocast(device_type=cls.device):
            with torch.no_grad():
                # Get the correspondent classification embedding from the head
                embeddings = cls.model(**encoded_data)[0][:, 0]

                norm_embeddings = torch.nn.functional.normalize(
                    embeddings, p=1, dim=1
                )
                return norm_embeddings.to("cpu")
