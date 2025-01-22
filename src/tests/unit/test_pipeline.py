from unittest import main, TestCase
from src.pipeline import SamplerTypes, JoinerTypes, SolverTypes
from src.tests.src.pipeline_mock import PipelineBuilderMock


class TestPipeline(TestCase):
    def test_can_define_pipelines(self):
        for sampler in SamplerTypes:
            for joiner in JoinerTypes:
                for solver in SolverTypes:
                    pipeline = PipelineBuilderMock.build(
                        sampler, joiner, solver
                    )
                    pipe_repr = {
                        "sampler": sampler,
                        "joiner": joiner,
                        "solver": solver,
                    }
                    self.assertDictEqual(pipe_repr, pipeline.config)


if __name__ == "__main__":
    main()
