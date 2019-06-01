from abc import ABC, abstractmethod
import soundfile as sf
import numpy as np

"""
    Generic class for handling audio files in the script.
"""
class IFileHelper(ABC):

    @abstractmethod
    def write_audio_file(self, filename: str, y:np.ndarray, fs:int):
        """
            Generic audio write method. 

            Parameters
            ----------
            filename: str
                Filepath for the output file
            y: np.ndarray
                Numpy array data to write as audio file. 
            fs: int
                Frequency sample: eg. 44100
        """
        pass

    @abstractmethod
    def read_audio_file(self, filename: str):
        """
            Generic audio read method. 

            Parameters
            ----------
            filename: str
                File path for the input file
            
            Returns
            -------
            It should return the numpy array of the read signal.
        """
        pass

    @abstractmethod
    def write_file(self, filename: str, data:np.ndarray):
        """
            Generic binary write method. It is used to restore the original hidden data: eg. .jpg, .png, .mp3...

            Parameters
            ----------
            filename: str
                File path for the output file with the extension: eg. photo.jpg
            data: np.ndarray:
                Numpy array data to write.
        """
        pass

    @abstractmethod
    def read_file(self, filename: str):
        """
            Generic binary read method. It is used to read the original message you want to encode: eg. .jpg, .png, .mp3...

            Parameters
            ----------
            filename: str
                File path for the input file with the extension: eg. photo.jpg
            
            Returns
            -------
            It should return the numpy array of the read binary file.
        """
        pass

    @abstractmethod
    def sum(self, base_file: str, encoded_file: str, output_file: str, message_location: int = 0):
        """
            Generic sum between signals. Here you must implement the way you wish to sum two signals hiding one in in another.

            Parameters
            ----------
            base_file: str
                File path for the carrier signal file.
            encoded_file: str
                Path of the encoded file you want to hide in base_file.
            output_file: str
                Path of the result output.
            message_location: int:
                Position in seconds in which you want to hide the message. The default position is 0s.
            
        """
        pass

    @abstractmethod
    def sub(self, output_file: str, base_file: str, restored_encoded_file: str, 
            message_width: int = 0, message_location: int = 0):
        """
            Generic subtraction between signals.

            Parameters
            ----------
            output_file: str
                Path of the result output.
            base_file: str
                File path for the original carrier signal file used in the 'sum' process.
            restored_encoded_file: str
                Path of the restored encoded file.
            message_width: int
                Message width of the hidden message, it must be known as a parameter used in the encoding process.
                Basically you must know how much is long (in samples) the file you hide in the carriel signal.
            message_location: int:
                Position in seconds in which you hide the message. The default position is 0s.
            
        """
        pass


class BinWav(IFileHelper):

    def __init__(self, pad_size:int=8):
        """
            Simple constructor which initialize the pad size for the binary read informations.

            Parameters
            ----------
            pad_size: int
                Number of zero-padding to add in the read bytes.
            
        """
        if pad_size<8:
            print("Warning, using a pad_size of %d can cause data loss."%(pad_size,))
        self.pad_size = pad_size

    def write_audio_file(self, filename: str, y, fs):
        """
            Write a wav file

            Parameters
            ----------
            filename: str
                Filepath for the output wav file
            y: np.ndarray
                Numpy array data to write as wav file. 
            fs: int
                Frequency sample: eg. 44100
        """
        sf.write(filename, y, fs)

    def read_audio_file(self, filename: str):
        """
            Read a wav file

            Parameters
            ----------
            filename: str
                File path for the input file
            
            Returns
            -------
            out : np.ndarray
                A numpy array containing the read wav samples, using soundfile it contains floats between 0 and 1.
        """
        return sf.read(filename)

    def write_file(self, filename: str, data:np.ndarray):
        """
            Write a binary file. It is not a generical method and it must be used with the encoded message.

            Parameters
            ----------
            filename: str
                File path for the restored data file with the extension: eg. photo.jpg
            data: np.ndarray:
                Numpy array data to write.
        """
        message: list = []
        for i in range(0, len(data), self.pad_size):
            s = '0b' + data[i:i + self.pad_size]
            message.append(int(s, 2))
        with open(filename, 'wb') as f:
            f.write(bytearray(message))
        
    def read_file(self, filename: str):
        """
            Read the original message you want to encode: eg. .jpg, .png, .mp3...
            It translate the read bytes to a message encoded as binary string sequence of 0 and 1.

            Parameters
            ----------
            filename: str
                File path for the input file with the extension: eg. photo.jpg
            
            Returns
            -------
            out: str
                The read file bytes as a string message of zeros and ones: eg. '1010101001010011100100'.
        """
        with open(filename, 'rb') as f:  # read binary data
            raw = f.read()
            data = ''.join([bin(raw[i])[2:].zfill(self.pad_size) for i in range(len(raw))])
        return data

    def sum(self, base_file: str, encoded_file: str, output_file: str, message_location: int = 0):
        """
            Sum between wav signals.

            Parameters
            ----------
            base_file: str
                File path for the carrier signal file.
            encoded_file: str
                Path of the encoded file you want to hide in base_file.
            output_file: str
                Path of the result output.
            message_location: int:
                Position in seconds in which you want to hide the message. The default position is 0s.
            
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
        """
            Subtraction between wav signals.

            Parameters
            ----------
            output_file: str
                Path of the result output.
            base_file: str
                File path for the original carrier signal file used in the 'sum' process.
            restored_encoded_file: str
                Path of the restored encoded file.
            message_width: int
                Message width of the hidden message, it must be known as a parameter used in the encoding process.
                Basically you must know how much is long (in samples) the file you hide in the carriel signal.
            message_location: int:
                Position in seconds in which you hide the message. The default position is 0s.
            
        """

        if not base_file:
            raise ValueError("Base file not found!")

        y0, fs0 = sf.read(base_file)
        y1, fs1 = sf.read(output_file)

        s1 = y1 - 0.25 * y0
        ss = s1[int(message_location * fs0):int(message_location * fs0) + message_width]

        # Writing File
        self.write_audio_file(restored_encoded_file, y=ss, fs=fs0)
