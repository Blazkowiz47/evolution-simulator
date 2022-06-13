import cv2
import numpy as np

WALL_PRESENT = 0x7FFFFFFF
CREATURE_ABSENT = 0

def importWorldFromImage(img_path: str):
    return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# 2147483647 / 0x7FFFFFFF are barriers


def createBarriers(grid: np.ndarray):
    for i in range(int(grid.shape[0]/4), int(grid.shape[0]*3/4)):
        grid[i][int(grid.shape[0]/4)] = 0x7FFFFFFF
    for i in range(int(grid.shape[0]/4), int(grid.shape[0]*3/4)):
        grid[i][int(grid.shape[0]*3/4)] = 0x7FFFFFFF
    return grid
