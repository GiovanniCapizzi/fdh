import numpy as np

from .config import Config

def modulate(data: str, conf: Config):
    ys = np.array([conf.sn0 if i == '1' else conf.sn1 for i in data])
    return ys.flatten()

def demodulate(encoded_file: str, conf: Config)->str:
    A, bp, t = conf.A, conf.bp, conf.t
    y, fs = conf.file_helper.read_audio_file(encoded_file)
    ss = len(conf.t)
    y0 = np.cos(2 * np.pi * conf.f0 * t)
    y1 = np.cos(2 * np.pi * conf.f1 * t)
    data = []
    for i in range(0, len(y), ss):
        sgl = y[i:i + ss]
        sgl0, sgl1 = sgl * y0, sgl * y1
        z0, z1 = np.trapz(sgl0, t), np.trapz(sgl1, t)
        z0, z1 = np.abs(np.ceil(2 * z0 / bp)), np.abs(np.ceil(2 * z1 / bp))
        if z0 > A / 2:
            data.append('1')
        elif z1 > A / 2:
            data.append('0')
    return "".join(data)

def encode(data_file: str, encoded_file: str, conf: Config):
    # Read data
    data = conf.file_helper.read_file(data_file)
    # Get the modulated signal
    ys = modulate(data, conf)
    # Writing the signal
    conf.file_helper.write_audio_file(encoded_file, y=ys, fs=int(conf.br))

def decode(encoded_file: str, decoded_file: str, conf: Config):
    conf.file_helper.write_file(decoded_file, demodulate(encoded_file, conf))
