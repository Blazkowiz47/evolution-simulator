from dataclasses import dataclass
import array as arr
import random as rd

from creatures.genome.gene import Gene, initialiseRandomGene, normaliseGeneIDs
from parameters.parameters import Parameter


@dataclass(frozen=True)
class Genome:
    genes: list[Gene]


# default total sinks and toal soruces are 128
# change this to get more number of valid identifiers
def initialiseRandomGenome(noOfGenes: int, params: Parameter):
    genes = []
    for _ in range(noOfGenes):
        genes.append(normaliseGeneIDs(
            gene=initialiseRandomGene(params=params), params=params))

    return Genome(genes=genes)
