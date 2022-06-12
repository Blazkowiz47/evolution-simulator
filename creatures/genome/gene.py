from dataclasses import dataclass
import random as rd
from creatures.brain.neurons import ActionNeurons, SensoryNeurons

from parameters.parameters import Parameter

# Gene identifies Sensory first,
# then Action
# and remaining are Computational Neurons


@dataclass(unsafe_hash=True)
class Gene:
    sinkType: int
    sinkId: int
    sourceType: int
    sourceId: int
    strength: int

    def __post_init__(self):
        assert(self.sinkId < 128)
        assert(self.sourceId < 128)
        assert(self.sinkType < 2)
        assert(self.sourceType < 2)
        assert(self.strength < 65536)


def initialiseRandomGene(params: Parameter):
    sn = SensoryNeurons.__len__()
    an = ActionNeurons.__len__()
    cn = params.totalComputationNeurons
    total = sn + an + cn
    sinkId = rd.randint(0, total)
    sourceId = rd.randint(0, total)

    sinkType = 0
    sourceType = 0
    if sinkId < sn + an and sinkId >= sn:
        sinkType = 1
    elif sinkId >= sn + an:
        sinkType = -1
    if sourceId < sn + an and sourceId >= sn:
        sourceType = 1
    elif sourceId >= sn + an:
        sourceType = -1
    return Gene(
        sinkType=sinkType,
        sourceType=sourceType,
        sinkId=sinkId,
        sourceId=sourceId,
        strength=rd.randint(0, 65535)
    )


def normaliseGeneIDs(gene: Gene, params: Parameter):

    sn = SensoryNeurons.__len__()
    an = ActionNeurons.__len__()
    cn = params.totalComputationNeurons
    total = sn + an + cn
    gene.sinkId = gene.sinkId % total
    gene.sourceId = gene.sourceId % total
    gene.sinkType = 0
    gene.sourceType = 0
    if gene.sinkId < sn + an and gene.sinkId >= sn:
        gene.sinkType = 1
    elif gene.sinkId >= sn + an:
        gene.sinkType = -1
    if gene.sourceId < sn + an and gene.sourceId >= sn:
        gene.sourceType = 1
    elif gene.sourceId >= sn + an:
        gene.sourceType = -1
    return gene
