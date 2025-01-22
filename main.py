from src.pipeline import PipelineBuilder, JoinerTypes, SamplerTypes, SolverTypes

if __name__ == "__main__":
    sampler = SamplerTypes.RANDOM
    joiner = JoinerTypes.WITH_SOURCE
    solver = SolverTypes.AS_IS
    pipe = PipelineBuilder.build(sampler, joiner, solver)

    headlines = [
        {"title": "Cruzeiro perde para o São Paulo na Copinha", "media": "G1"},
        {
            "title": "Cruzeiro e Atlético empatam sem gols nos EUA",
            "media": "ESPN",
        },
        {
            "title": "Gabigol comenta a sua estréia pelo Cruzeiro: Satisfeito",
            "media": "Estado de Minas",
        },
        {
            "title": "Matheus Pereira, do Cruzeiro, pede aumento salarial",
            "media": "Itatiaia",
        },
        {
            "title": "Cruzeiro ainda busca reforços nessa janela de transferência",
            "media": "O Tempo",
        },
    ]

    print(pipe.run(headlines))
