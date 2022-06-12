from creatures.genome.gene import Gene, initialiseRandomGene, normaliseGeneIDs
from creatures.genome.genome import Genome
from parameters.parameters import Parameter
import random as rd

# For Sexual Reproduction pass 2 different parents
# In case of Asexual reproduction pass same Genome as both parents


def generateChildGenome(parent1: Genome, parent2: Genome, params: Parameter):

    n1 = len(parent1.genes)
    n2 = len(parent2.genes)
    assert(n1 > 0)
    assert(n2 > 0)

    newGenome = None

    # randomly overlays slice of small or second parent
    # genes on first parent
    def overlayWithSlice(shorterGenome: Genome):
        st = rd.randint(0, len(shorterGenome.genes)-1)
        ed = rd.randint(0, len(shorterGenome.genes))
        if ed < st:
            t = ed
            ed = st
            st = t
        for i in range(st, ed):
            newGenome.genes[i] = shorterGenome.genes[i]

    if n1 < n2:
        newGenome = parent2
        overlayWithSlice(parent1)
    else:
        newGenome = parent1
        overlayWithSlice(parent2)

    assert(len(newGenome.genes) >= params.minGenomeLength)

    newGenome = randomInsertionDeletion(genome=newGenome, params=params)

    assert(len(newGenome.genes) >= params.minGenomeLength)

    for i, g in enumerate(newGenome.genes):
        newGenome.genes[i] = pointMutation(gene=g, params=params)

    assert(len(newGenome.genes) >= params.minGenomeLength)

    return newGenome

# can change default mutation probability


def pointMutation(gene: Gene, params: Parameter):

    mutation = 0

    for i in range(7):
        if rd.random() < params.mutationProbability:
            mutation += 1
            if i != 6:
                mutation << 1
        else:
            mutation += 0
            if i != 15:
                mutation << 1
    gene.sinkId = (gene.sinkId ^ mutation) % params.totalNeurons

    mutation = 0

    for i in range(7):
        if rd.random() < params.mutationProbability:
            mutation += 1
            if i != 6:
                mutation << 1
        else:
            mutation += 0
            if i != 15:
                mutation << 1
    gene.sourceId = gene.sourceId ^ mutation

    mutation = 0

    for i in range(16):
        if rd.random() < params.mutationProbability:
            mutation += 1
            if i != 15:
                mutation << 1
        else:
            mutation += 0
            if i != 15:
                mutation << 1
    gene.strength = gene.strength ^ mutation

    if rd.random() < params.mutationProbability:
        gene.sinkType = gene.sinkType ^ (rd.randint(0, 255) & 1)

    if rd.random() < params.mutationProbability:
        gene.sinkType = gene.sourceType ^ (rd.randint(0, 255) & 1)
    gene = normaliseGeneIDs(gene=gene, params=params)
    return gene

# Randomly insert new Gene or delete a gene


def randomInsertionDeletion(genome: Genome,  params: Parameter):

    if rd.randint(0, 255) & 1:
        if len(genome.genes) <= params.maxGenomeLength:
            if rd.random() < params.probabilityOfGeneInsertion:
                gene = initialiseRandomGene(params=params)
                gene = normaliseGeneIDs(gene=gene, params=params)
                genome.genes.append(gene)

    else:
        if rd.random() < params.probabilityOfGeneDeletion:
            if len(genome.genes) - 1 >= params.minGenomeLength:
                genome.genes.pop(rd.randint(0, len(genome.genes)-1))

    return genome
