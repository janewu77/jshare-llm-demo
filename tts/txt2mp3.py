import os
import asyncio
from my_tts.my_edge_tts import MyEdgeTTS
from my_tts.my_coqui_tts import MyCoquiTTSLocal
from my_tts.my_openai_tts import MyOPENAITTS
from my_tts.my_parler_tts import MyParlerTTSLocal

# 主要功能：
# 将一篇txt文档，按段落切分后生成tts


def merge_mp3(files, output_file):
    from pydub import AudioSegment
    """
    Merge multiple MP3 files into a single file.

    Parameters:
    files (list): List of file paths to the MP3 files.
    output_file (str): File path for the output merged MP3.
    """
    # Load the first file
    combined = AudioSegment.from_mp3(files[0])

    # Append each file to the combined file
    for file in files[1:]:
        next_audio = AudioSegment.from_mp3(file)
        combined += next_audio

    # Export the combined file
    combined.export(output_file, format="mp3")


def file_to_list(file_name):
    """
    Function to open a txt file, split it by paragraphs, and generate a list.

    Parameters:
    file_name (str): The name of the file to be opened.

    Returns:
    list: A list of paragraphs from the file, or None if the file is not found.
    """
    try:
        # Open the file in read mode
        with open(file_name, 'r', encoding='utf-8') as file:
            # Read the entire file content
            content = file.read()

            # Split the content by two consecutive newlines, which typically represent paragraph breaks
            paragraphs = content.split('\n\n')

        # Filter out empty paragraphs
        paragraphs = [para for para in paragraphs if para.strip()]
        return paragraphs

    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None


async def async_run(file_name, flag='edge'):

    paragraphs = file_to_list(file_name)
    filename_without_extension = os.path.splitext(os.path.basename(file_name))[0]
    mp3_files = []

    if paragraphs is not None:
        if flag == 'coqui':
            coqui_tts = MyCoquiTTSLocal()
        if flag == 'parler':
            parler_tts = MyParlerTTSLocal()
            # voice_desc_male = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, in a very confined sounding environment with clear audio quality. He speaks very fast."
            voice_desc_female = "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."

        for i, paragraph in enumerate(paragraphs, start=1):
            # print(f"text:{text}")
            # print(f"name:{name}")
            o_file_name = f"output/{filename_without_extension}/{flag}_{filename_without_extension}_{i}.mp3"
            if flag == 'coqui':
                # coqui
                voice = "en" # LJ025-0076 en jane_2
                output_file = coqui_tts.do_tts(paragraph, voice, o_file_name)
            elif flag == 'openai':
                voice = "shimmer" # alloy, echo, fable, onyx, nova, and shimmer
                output_file = MyOPENAITTS.do_tts(paragraph, voice, o_file_name)
            elif flag == 'parler':
                output_file = parler_tts.do_tts(paragraph, "", o_file_name, "", voice_desc_female)
            else:
                # edge
                output_file = await MyEdgeTTS.do_tts(paragraph, "en-US-SteffanNeural", o_file_name)

            print(f"output_file:{output_file}")
            mp3_files.append(output_file)

    return mp3_files


# 将txt文件转成mp3
def run_article2mp3(file_name, flag='edge'):
    # file_name = "aa.txt"
    # flag = "coqui"  # coqui edge openai
    mp3_files = asyncio.run(async_run(file_name, flag))

    # 将各段的mp3合并成一个文件
    filename_without_extension = os.path.splitext(os.path.basename(file_name))[0]
    merge_mp3(mp3_files, f"output/{filename_without_extension}/{flag}_{filename_without_extension}_combined.mp3")


def run_txt2mp3(paragraph, keyword, flag='edge'):

    output_file = f"output/{flag}_{keyword}.mp3"
    if flag == 'coqui':
        # coqui
        voice = "en"  # LJ025-0076 en jane_2
        coqui_tts = MyCoquiTTSLocal()
        output_file = coqui_tts.do_tts(paragraph, voice, output_file)
    elif flag == 'openai':
        # 'openai':
        voice = "shimmer"  # alloy, echo, fable, onyx, nova, and shimmer
        output_file = MyOPENAITTS.do_tts(paragraph, voice, output_file)
    elif flag == 'parler':
        parler_tts = MyParlerTTSLocal()
        # voice_desc_male = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, in a very confined sounding environment with clear audio quality. He speaks very fast."
        voice_desc_female = "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."
        output_file = parler_tts.do_tts(paragraph, "", output_file, "", voice_desc_female)
    else:
        # edge
        # MyEdgeTTS.do_tts_one(paragraph, "en-US-SteffanNeural", output_file)
        output_file = asyncio.run(MyEdgeTTS.do_tts(paragraph, "en-US-SteffanNeural", output_file))

    print(f"output_file:{output_file}")
    from tts.util.sound_util import play_sound
    play_sound(output_file)


if __name__ == "__main__":

    # # 处理一篇文章时，用
    file_name = "aa.txt"
    flag = "parler"  # coqui edge openai
    run_article2mp3(file_name, flag)

    # # 处理单个段
    # paragraph = '''
    #    The image displays a modern indoor café or break area bathed in natural light, which flows in through a large, curved glass wall offering a view of verdant trees and distant buildings. Inside, there are simple, white round tables paired with understated tan chairs, all arranged neatly within the space.
    # '''
    # keyword = "indoor"
    #
    # # coqui edge openai  parler
    # # coqui的句子单句不能超过250
    # flag = "parler"
    # run_txt2mp3(paragraph, keyword, flag)




