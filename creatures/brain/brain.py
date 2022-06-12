from dataclasses import dataclass, field
from creatures.brain.neurons import ActionNeurons, SensoryNeurons
from creatures.genome.genome import Genome


@dataclass
class Brain:
    genome: Genome
    wirings: list = field(init=False)

    def __post_init__(self):
        self.wirings = wireAsPerGenome(genome=self.genome)


@dataclass
class Neuron:
    weight: int
    source: any
    sink: any


def wireAsPerGenome(genome: Genome):
    wirings = []
    sn = SensoryNeurons.__len__()
    an = ActionNeurons.__len__()
    for gene in genome.genes:
        # if gene has source of computational neurons
        # or Action neurons continue to next gene
        if gene.sourceType != 0:
            continue
        # if sink is a source neuron
        # continue to next gene
        if gene.sinkType == 0:
            continue
        temp = []
        # if sink is ActionNeuron wiring for this
        # is complete
        if gene.sinkType == 1:
            temp.append(Neuron(weight=gene.strength,
                               source=SensoryNeurons(gene.sourceId+1),
                               sink=ActionNeurons(
                                   gene.sinkId + 1 - sn)
                               ))
            wirings.append(temp)
            continue
        # Else if it is a Computational Neuron
        # find the chain
        temp.append(Neuron(weight=gene.strength,
                           source=SensoryNeurons(gene.sourceId+1),
                           sink=gene.sinkId + 1 - sn - an
                           ))
        nextId = gene.sinkId

        while nextId:
            flag = True
            # Find the gene with source as previous sink
            for g in genome.genes:
                if g.sourceId == nextId:
                    if g.sinkId == g.sourceId:
                        continue
                    if g.sinkType == 0:
                        # If the gene has sink as Sensory Neuron
                        # continue to next gene
                        continue
                    elif g.sinkType == -1:
                        # If it is connected to another Computational Neuron
                        # Append and update the previous source id
                        # first check whether the wirings dont form a loop
                        check = False
                        for n in temp:
                            if n.source == g.sinkId+1-an-sn:
                                check = True
                                break
                        if check:
                            continue

                        temp.append(
                            Neuron(
                                weight=g.strength,
                                source=nextId + 1 - sn - an,
                                sink=g.sinkId + 1 - an - sn
                            )
                        )

                        flag = False
                        nextId = g.sinkId
                    else:
                        # if sink is Action wiring is complete
                        temp.append(
                            Neuron(
                                weight=g.strength,
                                source=nextId + 1 - sn - an,
                                sink=ActionNeurons(g.sinkId + 1 - sn)
                            )
                        )
                        wirings.append(temp)
                        break

            if flag:
                break
    return wirings
