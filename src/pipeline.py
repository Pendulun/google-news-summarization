from dataclasses import dataclass
import enum
from typing import Callable

from clustered_sampling import ClusteredSample
from joiner import join_headlines, join_headlines_with_source
from sampling import sample
from solvers import present_as_is


@dataclass
class Runner:
    callable_func: Callable
    name: enum.Enum


class SamplerTypes(enum.Enum):
    RANDOM = 1
    CLUSTER_SAMPLER = 2
    AS_IS = 3


class JoinerTypes(enum.Enum):
    WITH_SOURCE = 1
    AS_IS = 2


class SolverTypes(enum.Enum):
    LLM_SUMMARIZATION = 1
    LLM_CHAT = 2
    AS_IS = 3


class Pipeline:
    def __init__(self):
        self._sampler: Runner = None
        self._joiner: Runner = None
        self._solver: Runner = None

    @property
    def sampler(self) -> Runner:
        return self._sampler

    @property
    def joiner(self) -> Runner:
        return self._joiner

    @property
    def solver(self) -> Runner:
        return self._solver

    @sampler.setter
    def sampler(self, new_sampler: Runner):
        self._sampler = new_sampler

    @joiner.setter
    def joiner(self, new_joiner: Runner):
        self._joiner = new_joiner

    @solver.setter
    def solver(self, new_solver: Runner):
        self._solver = new_solver

    @property
    def config(self) -> dict:
        return {
            "solver": self._solver.name,
            "joiner": self._joiner.name,
            "sampler": self._sampler.name,
        }


class PipelineBuilder:
    @classmethod
    def build(
        cls, sampler: SamplerTypes, joiner: JoinerTypes, solver: SolverTypes
    ) -> Pipeline:

        sampler_map = {
            SamplerTypes.RANDOM: sample,
            SamplerTypes.CLUSTER_SAMPLER: ClusteredSample,
            SamplerTypes.AS_IS: lambda x: x,
        }

        joiner_map = {
            JoinerTypes.AS_IS: join_headlines,
            JoinerTypes.WITH_SOURCE: join_headlines_with_source,
        }

        solver_map = {
            SolverTypes.AS_IS: present_as_is,
            SolverTypes.LLM_SUMMARIZATION: present_as_is,
            SolverTypes.LLM_CHAT: present_as_is,
        }

        pipeline = Pipeline()
        pipeline.sampler = Runner(sampler_map[sampler], sampler)
        pipeline.joiner = Runner(joiner_map[joiner], joiner)
        pipeline.solver = Runner(solver_map[solver], solver)
        return pipeline
