import os
import numpy as np
import cv2


def saveFrame(dir: str, number: int, image: np.ndarray):
    cv2.imwrite(dir+'/{}.png'.format(number), image)


def convertFramesToVideo(dir: str):

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(
        dir+'/result.avi', fourcc, 30, size)
    size = None
    for f in os.listdir(dir):
        image = cv2.imread(dir + '/'+f)

        size = (image.shape[0], image.shape[1])
        for _ in range(6):
            out.write(image)

    out.release()
