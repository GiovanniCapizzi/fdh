# On the installed version
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
