from dataclasses import dataclass

import numpy as np
from .file_helper import IFileHelper

@dataclass
class Config:
    A: float
    bp: float
    br: float
    f0: float
    f1: float
    rp: float
    t: np.ndarray
    sn0: float
    sn1: float
    file_helper: IFileHelper

def make_config(file_helper: IFileHelper,
                amplitude: float = 0.0001,
                bit_period: float = 1 / 44100,
                redundancy: int = 2 ) -> Config:

    br = 1 / bit_period  # bit rate, 1MHz per sec
    f0 = br * redundancy
    f1 = br * (redundancy / 2)
    rp = bit_period / (redundancy * 2)
    t = np.arange(rp, bit_period + rp, rp)
    sn0 = amplitude * np.cos(2 * np.pi * f0 * t)
    sn1 = amplitude * np.cos(2 * np.pi * f1 * t)

    return Config(amplitude, bit_period, br, f0, f1, rp, t, sn0, sn1, file_helper)
