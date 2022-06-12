import os
import logging
from dataclasses import dataclass, field

from creatures.brain.neurons import ActionNeurons, SensoryNeurons


@dataclass
class Parameter:
    population: int = field(default=200)
    stepsPerGeneration: int = field(default=100)
    maxGenerations: int = field(default=100)
    numThreads: int = field(default=4)
    totalComputationNeurons: int = field(default=10)

    # Should not be changed after initialisation
    sizeX: int = field(default=200)
    sizeY: int = field(default=200)
    logDir: str = field(default="./logs")
    imageDir: str = field(default="./images")
    genomeInitialLengthMin: int = field(default=2)
    genomeInitialLengthMax: int = field(default=10)
    mutationProbability: float = field(default=0.001)
    probabilityOfGeneInsertion: float = field(default=0.0001)
    probabilityOfGeneDeletion: float = field(default=0.0001)
    maxGenomeLength: int = field(default=7)
    minGenomeLength: int = field(default=1)
    survival_criteria: int = field(default=1)
    maxChildren: int = field(default=3)

    # auto uppdates
    parameterChangeGenerationNumber: int = field(default=0, init=False)
    # intrinsic
    totalIONeurons: int = field(default=2, init=False)
    totalNeurons: int = field(default=2, init=False)

    def __post_init__(self):
        self.totalIONeurons = SensoryNeurons.__len__() + ActionNeurons.__len__()
        self.totalNeurons = self.totalIONeurons + self.totalComputationNeurons

    def checkDirsExists(self):
        if not os.path.exists(self.logDir):
            try:
                os.makedirs(self.logDir)
            except:
                logging.debug(
                    "Log Directory doesnot exist and cannot be created")
                raise
        if not os.path.exists(self.imageDir):
            try:
                os.makedirs(self.imageDir)
            except:
                logging.debug(
                    "Log Directory doesnot exist and cannot be created")
                raise
