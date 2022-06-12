import logging
import numpy as np
from parameters.parameters import Parameter


def dualWorld(sizeX: int, sizeY: int):
    grid = np.ndarray((sizeX, sizeY), dtype=np.int8)
    for i in range(sizeY):
        for j in range(int(sizeX/2)):
            grid[i][j] = -1
    return grid


def getSurvivalCriteria(params: Parameter):
    if params.survival_criteria == 1:
        return dualWorld(params.sizeX, params.sizeY)
    else:
        logging.debug('Invalid Survival Criteria.')
        raise
