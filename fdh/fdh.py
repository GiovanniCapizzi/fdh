import numpy as np

from .config import Config


def modulate(data: str, conf: Config):
    """
    Raw implementation of modulation using two sinewaves from a configuration object. 
    It encodes '1' with the 'sn0' sinewave, and '0' with the 'sn1' sinewave.
    
    Parameters
    ----------
    data: str
        String representation of the binary message: eg. '101001010'.
    conf: Config
        Configuration instance of fdh.Config class.

    Returns
    -------
    out: np.ndarray
        Numpy array for the encoded message. This array contains an alternation of 'sn0' and 'sn1' sinewaves values. 
    """
    ys = np.array([conf.sn0 if i == '1' else conf.sn1 for i in data])
    return ys.flatten()

def demodulate(encoded_file: str, conf: Config)->str:
    """
    Raw implementation of the fsk demodulation. 
    Using two sinewaves from a configuration object, it calculates which sinewave is contained in the message.
    It decodes 'ones' if 'sn0' sinewave is found, otherwise yields 'zeros'.
    
    Parameters
    ----------
    encoded_file: str
        Path of the encoded file.
    conf: Config
        Configuration instance of fdh.Config class.

    Returns
    -------
    out: str
        String representation of the decoded binary message: eg. '101001010'.
    """
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
    """
    Encode the original file applying the modulation to the binary representation of the signal.
    It saves the result in the encoded_file path.
    
    Parameters
    ----------
    data_file: str
        Path of the file to encode.
    encoded_file: str
        Path of the output file.
    conf: Config
        Configuration instance of fdh.Config class.

    Returns
    -------
    None
    
    """
    # Read data
    data = conf.file_helper.read_file(data_file)
    # Get the modulated signal
    ys = modulate(data, conf)
    # Writing the signal
    conf.file_helper.write_audio_file(encoded_file, y=ys, fs=int(conf.br))

def decode(encoded_file: str, decoded_file: str, conf: Config):
    """
    Restore the original file applying the decoding process to the encoded_file.
    
    Parameters
    ----------
    encoded_file: str
        Path of the input file.
    decoded_file: str
        Path of the output restored file.
    conf: Config
        Configuration instance of fdh.Config class.

    Returns
    -------
    None
    
    """
    conf.file_helper.write_file(decoded_file, demodulate(encoded_file, conf))
