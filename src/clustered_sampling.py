import random

import numpy as np
from sklearn.cluster import DBSCAN
import torch
from torch.utils.data import Dataset, DataLoader
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModel


class HeadlinesDataset(Dataset):
    def __init__(self, headlines: list[str]):
        self.headlines = np.array(headlines)

    def __len__(self):
        return len(self.headlines)

    def __getitem__(self, idx) -> tuple[list[str], str]:
        if torch.is_tensor(idx):
            idx = idx.tolist()

        data = self.headlines[idx]

        if len(data) > 1:
            return self.headlines[idx].tolist()
        else:
            return [data]


class ClusteredSample:
    model = None
    tokenizer = None
    device = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    def set_model(cls, model_name: str):
        cls.tokenizer = AutoTokenizer.from_pretrained(model_name)
        cls.model = AutoModel.from_pretrained(model_name).to(cls.device)

    @classmethod
    def get_embeddings_from_model(cls, data: list[str]):
        encoded_data = cls.tokenizer(
            data, padding=True, truncation=True, return_tensors="pt"
        ).to(cls.device)
        with torch.autocast(device_type=cls.device):
            with torch.no_grad():
                # Get the correspondent classification embedding from the head
                embeddings = cls.model(**encoded_data)[0][:, 0]

                norm_embeddings = torch.nn.functional.normalize(
                    embeddings, p=1, dim=1
                )
                return norm_embeddings.to("cpu")

    @classmethod
    def clustered_sample(cls, headlines: list[str], batch_size: int = 32):
        dataset = HeadlinesDataset(headlines)
        np_embs = cls.get_embeddings(dataset, batch_size)
        clustering = DBSCAN(eps=3, min_samples=2, n_jobs=-1).fit(np_embs)
        sampled = list()
        for label in np.unique(clustering.labels_):
            cluster_data = dataset[np.where(clustering.labels_ == label)]
            sampled.append(random.choice(cluster_data))
        return sampled

    @classmethod
    def get_embeddings(cls, dataset, batch_size: int = 16) -> np.ndarray:
        embeddings = list()
        for i, batch in tqdm(
            enumerate(DataLoader(dataset, batch_size=batch_size)),
            desc="Calc embeddings",
        ):
            embs = cls.get_embeddings_from_model(batch)
            embeddings.append(embs)

        np_embs = torch.cat(embeddings).numpy()
        return np_embs
