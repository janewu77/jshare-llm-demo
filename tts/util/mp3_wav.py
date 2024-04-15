from pydub import AudioSegment
# pip install pydub


def mp3_2_wav(mp3_file, wav_file):
    mp3_audio = AudioSegment.from_file(mp3_file, format="mp3")

    # 转换为WAV
    mp3_audio.export(wav_file, format="wav")


def wav_2_mp3(wav_file, mp3_file):
    # 读取WAV文件
    wav_audio = AudioSegment.from_file(wav_file, format="wav")

    # 转换为MP3
    wav_audio.export(mp3_file, format="mp3")


if __name__ == "__main__":
    mp3_2_wav("jane_1.mp3", "jane_1.wav")


