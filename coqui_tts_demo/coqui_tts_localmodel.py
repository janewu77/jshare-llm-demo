import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

from datetime import datetime
from dateutil import rrule


class MyCoquiTTSLocal:
    # 指定本地模型
    model_path = "/Users/jingwu/janewu/llm-model/coqui/XTTS-v2"

    model = None
    gpt_cond_latent = None
    speaker_embedding = None
    config = XttsConfig()

    gpt_cond_latent_s = {}
    speaker_embedding_s = {}

    # def __init__(
    #     self,
    #     model_name: str = "",
    #     model_path: str = None,
    #     config_path: str = None,
    #     vocoder_path: str = None,
    #     vocoder_config_path: str = None,
    #     progress_bar: bool = True,
    #     gpu=False,
    # ):
    def __init__(self):
        # global model, gpt_cond_latent, speaker_embedding, config
        print("Loading model...")
        # config = XttsConfig()
        self.config.load_json(f"{self.model_path}/config.json")
        self.model = Xtts.init_from_config(self.config)
        self.model.load_checkpoint(self.config, checkpoint_dir=self.model_path, eval=True)  # , use_deepspeed=True)
        # model.cuda()
        # model.mps()

    def compute_latents(self, lang):
        if lang in self.gpt_cond_latent_s and lang in self.speaker_embedding_s:
            return self.gpt_cond_latent_s[lang], self.speaker_embedding_s[lang]

        print("Computing speaker latents...")
        gpt_cond_latent, speaker_embedding = self.model.get_conditioning_latents(
            audio_path=[f"{self.model_path}/samples/{lang}_sample.wav"])

        # 指定中文 的参考声音
        # gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["sample_cn.wav"])

        self.gpt_cond_latent_s[lang] = gpt_cond_latent
        self.speaker_embedding_s[lang] = speaker_embedding
        return self.gpt_cond_latent_s[lang], self.speaker_embedding_s[lang]

    def do_tts(self, text, voice, output_file, lang):
        start_time = datetime.now()
        print(f"Inference...{lang}")


        gpt_cond_latent, speaker_embedding = self.compute_latents(lang)
        out = self.model.inference(
            text,
            lang,
            gpt_cond_latent,
            speaker_embedding,
            temperature=0.1,  # Add custom parameters here
        )

        torchaudio.save(output_file, torch.tensor(out["wav"]).unsqueeze(0), 24000)
        seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
        print(f"total spend: {seconds.count()} seconds")


# def do_tts2(prompt_txt, output_wave_fn):
#     # 没有仔细测。不太好用的样子
#     print("synthesize...")
#     start_time = datetime.now()
#     out = model.synthesize(
#         prompt_txt,
#         config,
#         speaker_wav="sample_cn.wav",
#         gpt_cond_len=3,
#         language=lang,
#     )
#     torchaudio.save(output_wave_fn, torch.tensor(out["wav"]).unsqueeze(0), 24000)
#     seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
#     print(f"total spend: {seconds.count()} seconds")


if __name__ == '__main__':
    # global lang
    # xlang = 'en'  #
    xlang = 'zh-cn'

    myCoquiTTSLocal = MyCoquiTTSLocal()

    # prompt_txt = '''
    # It took me quite a long time to develop a voice and now that I have it I am not going to be silent.
    # '''
    prompt_txt = '''
    The word excursion refers to a short journey or trip, especially one taken as a leisure activity. 
    It typically involves going to a different place, often for enjoyment or educational purposes, and returning within a short period, like within a day.
    '''  # 27s
    # prompt_txt = '''
    # We explore how generating a chain of thought—a series of intermediate reasoning steps—significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain-of-thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting.
    #
    # Experiments on three large language models show that chain-of-thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. The empirical gains can be striking. For instance, prompting a PaLM 540B with just eight chain-of-thought exemplars achieves state-of-the-art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier.
    # '''
    prompt_txt_cn = '''
    我是在线客服，由公司的开发团队开发。 很抱歉，我无法提供开发者的联系方式。
    '''  # 13s
    myCoquiTTSLocal.do_tts(prompt_txt_cn, "", f"output/xtts_{xlang}.wav", xlang)

    prompt_txt_cn = '''
    我是在线客服，由公司的开发团队开发。 很抱歉，我无法提供开发者的联系方式。
    '''  # 13s
    myCoquiTTSLocal.do_tts(prompt_txt_cn, "", f"output/xtts_{xlang}.wav", xlang)

    # prompt_txt = '''
    # 我是在线客服，由公司的开发团队开发。 很抱歉，我无法提供开发者的联系方式。
    # '''
    # lang = 'en'  # zh-cn
    # do_tts(prompt_txt, "zh-cn", "xtts_cn.wav")


