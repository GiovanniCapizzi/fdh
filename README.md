<p align="center">
  <img width="256" src="https://raw.githubusercontent.com/GiovanniCapizzi/fdh/master/assets/logo.png">
</p>

# Frequency Shift Keying for Data Hiding
[![Build Status](https://travis-ci.org/GiovanniCapizzi/fdh.svg?branch=master)](https://travis-ci.org/GiovanniCapizzi/fdh)
### Requirements
Python 3.7

### Install
```bash
pip install numpy
pip install soundfile
python setup.py install
```

### Usage 
```python
from fdh import BinWav, make_config, encode, decode

if __name__ == "__main__":
    helper = BinWav(pad_size=8)
    conf = make_config(file_helper=helper, amplitude=0.0001, bit_period=1 / 44100, redundancy=2)

    print(" >> Encode")
    encode("../assets/data.jpg", "./encoded_message.wav", conf)

    print(" >> Decode")
    decode("./encoded_message.wav", "./data_restored.jpg", conf)

    print(" >> Sum")
    width = helper.sum("../assets/clip.wav", "./encoded_message.wav", './output_fsk.wav')

    print(" >> Sub")
    helper.sub('./output_fsk.wav', "../assets/clip.wav", "./restored_encoded_message.wav", message_width=width)

    print(" >> Restore")
    decode("./restored_encoded_message.wav", "./data_restored.jpg", conf)

```

### Based on:
[fsk modulation written matlab](https://it.mathworks.com/matlabcentral/fileexchange/44821-matlab-code-for-fsk-modulation-and-demodulation)

### Binary resources are taken from: 
[audio clip](https://freesound.org/people/InspectorJ/sounds/406085/)

[image](https://www.publicdomainpictures.net/ru/view-image.php?image=35696)

