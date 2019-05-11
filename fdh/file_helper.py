from abc import ABC, abstractmethod
import soundfile as sf
import numpy as np


class IFileHelper(ABC):

    @abstractmethod
    def write_audio_file(self, filename: str, y, fs):
        pass

    @abstractmethod
    def read_audio_file(self, filename: str):
        pass

    @abstractmethod
    def write_file(self, filename: str, data:np.ndarray):
        pass

    @abstractmethod
    def read_file(self, filename: str):
        pass

    @abstractmethod
    def sum(self, base_file: str, encoded_file: str, output_file: str, message_location: int = 0):
        pass

    @abstractmethod
    def sub(self, output_file: str, base_file: str, restored_encoded_file: str, 
            message_width: int = 0, message_location: int = 0):
        pass


class BinWav(IFileHelper):

    def __init__(self, pad_size:int=8):
        if pad_size<8:
            print("Warning, using a pad_size of %d can cause data loss."%(pad_size,))
        self.pad_size = pad_size

    def write_audio_file(self, filename: str, y, fs):
        sf.write(filename, y, fs)

    def read_audio_file(self, filename: str):
        return sf.read(filename)

    def write_file(self, filename: str, data:np.ndarray):
        """
            filename: the output file path for the restored data
        """
        message: list = []
        for i in range(0, len(data), self.pad_size):
            s = '0b' + data[i:i + self.pad_size]
            message.append(int(s, 2))
        with open(filename, 'wb') as f:
            f.write(bytearray(message))
        
    def read_file(self, filename: str):
        """
            filename: the input file path to encode with fsk
        """
        with open(filename, 'rb') as f:  # read binary data
            raw = f.read()
            data = ''.join([bin(raw[i])[2:].zfill(self.pad_size) for i in range(len(raw))])
        return data

    def sum(self, base_file: str, encoded_file: str, output_file: str, message_location: int = 0):
        """
            filename: base_file: the audio file in which hide the encoded_file
            message_location: message position in time (expressed in seconds)
        """
        if not base_file:
            raise ValueError("Base file not found!")

        y0, fs0 = sf.read(base_file)
        y1, fs1 = sf.read(encoded_file)

        if message_location > y0.size - y1.size:
            raise ValueError("Message location is out of bound for base_file.")

        if y0.size < y1.size:
            raise ValueError("Base file is too short for this message!")

        if fs0 != fs1:
            raise ValueError("Can't use different frequency samples!")

        s1 = np.zeros(y0.size)      
        message_width = y1.size  # in samples!

        s1[int(message_location * fs0):int(message_location * fs0) + message_width] = y1
        ss = s1 + 0.25 * y0

        # Writing File
        self.write_audio_file(output_file, y=ss, fs=fs0)
        return message_width

    def sub(self, output_file: str, base_file: str, restored_encoded_file: str, 
            message_width: int = 0, message_location: int = 0):

        if not base_file:
            raise ValueError("Base file not found!")

        y0, fs0 = sf.read(base_file)
        y1, fs1 = sf.read(output_file)

        s1 = y1 - 0.25 * y0
        ss = s1[int(message_location * fs0):int(message_location * fs0) + message_width]

        # Writing File
        self.write_audio_file(restored_encoded_file, y=ss, fs=fs0)
