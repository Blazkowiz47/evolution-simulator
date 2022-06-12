import os
from tqdm import tqdm
import numpy as np
import cv2


def saveFrame(dir: str, number: int, image: np.ndarray):
    cv2.imwrite(dir+'/{}.png'.format(number), image)


def convertFramesToVideo(dir: str, size: tuple, end: int):

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(
        dir+'/result.avi', fourcc, 60, size)
    for i in tqdm(range(1, end), "Frames processed "):
        image = cv2.imread(dir+'/'+str(i)+'.png')
        out.write(image)
        os.remove(dir+'/'+str(i)+'.png')
    # with os.scandir(dir) as it:
    #     for f in it:
    #         if 'png' in f.name:
    #             image = cv2.imread(f.path)
    #             out.write(image)
    #             os.remove(f.path)
    out.release()
