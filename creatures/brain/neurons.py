from enum import Enum


class SensoryNeurons(Enum):
    LOC_X = 1   # X displacement of creature from top left
    LOC_Y = 2   # Y displacement of creature from top left
    W = 3       # Population Density in the Neighbour-hood
    AGE = 4     # Age of creature
    LAST_MOVE_X = 5
    LAST_MOVE_Y = 6


class ActionNeurons(Enum):
    MOV_L = 1   # Move creature left
    MOV_R = 2   # Move creature right
    MOV_U = 3   # Move creature up
    MOV_D = 4   # Move creature down
    MOV_Rn = 5  # Move creature Random
    KILL = 6    # Kill adjacent creature
