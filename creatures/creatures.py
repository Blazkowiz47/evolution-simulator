from dataclasses import dataclass, field
from creatures.brain.brain import Brain
from creatures.genome.genome import Genome


@dataclass()
class Creature:
    genome: Genome
    location: tuple
    last_location: tuple
    brain: Brain = field(init=False)
    alive: bool = field(default=True, init=False)
    age: int = field(default=0, init=False)
    score: float = field(init=False, default=0.0)

    def __post_init__(self):
        self.brain = Brain(genome=self.genome)
