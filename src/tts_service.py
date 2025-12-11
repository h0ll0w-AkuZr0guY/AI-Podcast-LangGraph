import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class TTSService:
    def __init__(self):
        # 配置dashscope API
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        dashscope.api_key = self.api_key
        
        # 设置模型和音色
        self.model = os.getenv("DASHSCOPE_MODEL", "cosyvoice-v2")
        self.voice = os.getenv("DASHSCOPE_VOICE", "longxiaochun_v2")
    
    def text_to_speech(self, text: str, output_file: str = "output.mp3") -> bool:
        """
        将文本转换为语音并保存到文件
        
        Args:
            text: 要转换的文本
            output_file: 输出音频文件路径
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            # 每次调用时创建新的SpeechSynthesizer实例
            synthesizer = SpeechSynthesizer(model=self.model, voice=self.voice)
            
            # 调用dashscope API进行语音合成
            audio = synthesizer.call(text)
            
            # 保存音频文件
            with open(output_file, "wb") as f:
                f.write(audio)
            
            # 打印首包延迟信息
            print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
                synthesizer.get_last_request_id(),
                synthesizer.get_first_package_delay()))
            
            print(f"语音合成成功，音频文件已保存至: {output_file}")
            return True
        
        except Exception as e:
            print(f"语音合成失败: {str(e)}")
            return False
    
    def batch_text_to_speech(self, text_list: list, output_dir: str = "output") -> list:
        """
        批量将文本转换为语音
        
        Args:
            text_list: 文本列表
            output_dir: 输出目录
            
        Returns:
            生成的音频文件路径列表
        """
        # 创建输出目录（如果不存在）
        os.makedirs(output_dir, exist_ok=True)
        
        output_files = []
        
        for i, text in enumerate(text_list):
            output_file = os.path.join(output_dir, f"audio_{i+1}.mp3")
            if self.text_to_speech(text, output_file):
                output_files.append(output_file)
        
        return output_files


if __name__ == "__main__":
    tts = TTSService()
    tts.text_to_speech("你好，这是一个测试")