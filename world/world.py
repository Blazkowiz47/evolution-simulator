from dataclasses import dataclass, field
from world.world_utils import importWorldFromImage
import numpy as np


@dataclass
class World:
    width: int
    height: int
    grid: np.ndarray = field(init=False)
    img_path: str = field(default=None)

    def __post_init__(self):
        if self.img_path:
            self.grid = importWorldFromImage(img_path=self.img_path)
        else:
            self.grid = np.zeros((self.height, self.width), dtype=np.int32)


