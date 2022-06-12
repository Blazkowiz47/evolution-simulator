import logging
from parameters.parameters import Parameter


class ParamManager:

    def __init__(self, configFileName: str):
        # loads default _params
        self._params = Parameter()
        # updates config _params
        self._loadFromConfig(configFileName)
        self._params.checkDirsExists()

    def _loadFromConfig(self, configFileName: str):
        with open(configFileName, 'r') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for line in lines:
                if line == "\n" or len(line) == 0 or line[0] == "#":
                    continue
                extract = line.split("=")
                self._ingestParam(extract[0].rsplit()[
                                  0], extract[1].rsplit()[0])

    def _ingestParam(self, name: str, value: str):
        if name == "population":
            self._params.population = int(value)
        elif name == "stepsPerGeneration":
            self._params.stepsPerGeneration = int(value)
        elif name == "noOfGenerations":
            self._params.maxGenerations = int(value)
        elif name == "numThreads":
            self._params.numThreads = int(value)
        elif name == "sizeX":
            self._params.sizeX = int(value)
        elif name == "sizeY":
            self._params.sizeY = int(value)
        elif name == "logDir":
            self._params.logDir = value
        elif name == "imageDir":
            self._params.imageDir = value
        elif name == "genomeInitialLengthMin":
            self._params.genomeInitialLengthMin = int(value)
        elif name == "genomeInitialLengthMax":
            self._params.genomeInitialLengthMax = int(value)
        elif name == "sruvival_criteria":
            self._params.sruvival_criteria = int(value)
        elif name == "maxChildren":
            self._params.maxChildren = int(value)
        else:
            logging.debug("Invalid parameter " + name + " with value " + value)

    @property
    def params(self):
        return self._params
