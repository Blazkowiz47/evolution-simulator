import logging
import os
from tqdm import tqdm
import numpy as np
import cv2

# from world.world_utils import CREATURE_ABSENT, WALL_PRESENT


def saveFrame(dir: str, name: str, image: np.ndarray):
    # for i in range(image.shape[0]):
    #     for j in range(image.shape[1]):
    #         if image[i][j] != CREATURE_ABSENT and image[i][j] != WALL_PRESENT:
    #             image[i][j] = WALL_PRESENT
    cv2.imwrite(dir + '/' + name + '.png', image)


def convertFramesToVideo(dir: str, size: tuple, end: int):

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(
        dir+'/result.avi', fourcc, 60, size)
    for i in tqdm(range(end), "Frames processed "):
        image = cv2.imread(dir+'/'+str(i)+'.png')
        out.write(image)
        os.remove(dir+'/'+str(i)+'.png')

    # for f in tqdm(os.listdir(dir), "Frames processed "):
    #     if 'png' in f:
    #         image = cv2.imread(dir+'/'+f)
    #         out.write(image)
    #         os.remove(dir+'/'+f)

    # with os.scandir(dir) as it:
    #     for f in it:
    #         if 'png' in f.name:
    #             image = cv2.imread(f.path)
    #             out.write(image)
    #             os.remove(f.path)
    out.release()
