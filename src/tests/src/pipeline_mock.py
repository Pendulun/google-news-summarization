from typing import Callable
from pipeline import PipelineBuilder, SamplerTypes
from sampling import sample
from tests.src.clustered_sampling_mock import ClusteredSampleMock


class PipelineBuilderMock(PipelineBuilder):
    @classmethod
    def sampler_map(cls) -> dict[SamplerTypes, Callable]:
        sampler_map = {
            SamplerTypes.RANDOM: sample,
            SamplerTypes.CLUSTER_SAMPLER: ClusteredSampleMock,
            SamplerTypes.AS_IS: lambda x: x,
        }
        return sampler_map
