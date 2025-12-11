import os
from datetime import datetime
from src.text_processing import TextProcessor
from src.tts_service import TTSService
import src.config as config

class BlogGenerator:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.tts_service = TTSService()
    
    def generate_blog(self, topic: str, length: str = "medium", with_tts: bool = True) -> dict:
        """
        根据主题生成完整的博客内容，包括文本润色和可选的语音合成
        
        Args:
            topic: 博客主题
            length: 博客长度，可选值：short, medium, long
            with_tts: 是否生成语音文件
            
        Returns:
            包含博客信息的字典，格式：
            {
                "topic": 主题,
                "original_text": 原始生成文本,
                "polished_text": 润色后文本,
                "blog_file": 博客文件路径,
                "audio_file": 音频文件路径（如果生成）
            }
        """
        # 1. 根据主题生成原始博客内容
        print(f"正在根据主题 '{topic}' 生成博客内容...")
        original_text = self.text_processor.generate_blog_from_topic(topic, length)
        
        # 2. 对生成的内容进行润色
        print("正在润色博客内容...")
        polished_text = self.text_processor.polish_text(original_text, "blog")
        
        # 3. 保存博客文本到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blog_file = f"{config.RESULTS_DIR}/blog_{timestamp}.md"
        
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(f"# {topic}\n\n")
            f.write(polished_text)
        
        print(f"博客文本已保存至: {blog_file}")
        
        # 4. 生成语音文件（如果需要）
        audio_file = None
        if with_tts:
            print("正在生成语音文件...")
            audio_file = f"{config.RESULTS_DIR}/audio_{timestamp}.wav"
            self.tts_service.text_to_speech(polished_text, audio_file)
        
        return {
            "topic": topic,
            "original_text": original_text,
            "polished_text": polished_text,
            "blog_file": f"{config.RESULTS_DIR}/{blog_file}",
            "audio_file": f"{config.RESULTS_DIR}/{audio_file}" if audio_file else None
        }
    
    def polish_and_tts(self, original_text: str, polish_type: str = "blog", output_file: str = None) -> dict:
        """
        对已有文本进行润色并生成语音
        
        Args:
            original_text: 原始文本
            polish_type: 润色类型
            output_file: 自定义输出文件名（可选）
            
        Returns:
            包含处理结果的字典
        """
        # 1. 文本润色
        print("正在润色文本...")
        polished_text = self.text_processor.polish_text(original_text, polish_type)
        
        # 2. 生成语音文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not output_file:
            output_file = f"{config.RESULTS_DIR}/audio_{timestamp}.wav"
        
        print("正在生成语音文件...")
        success = self.tts_service.text_to_speech(polished_text, output_file)
        audio_file = f"{output_file}" if success else None
        
        return {
            "original_text": original_text,
            "polished_text": polished_text,
            "audio_file": audio_file,
            "success": success
        }
    
    def process_existing_blog(self, blog_file: str, with_tts: bool = True) -> dict:
        """
        处理已有的博客文件，进行润色和可选的语音合成
        
        Args:
            blog_file: 已有博客文件路径
            with_tts: 是否生成语音文件
            
        Returns:
            包含处理结果的字典
        """
        # 1. 读取博客文件
        if not os.path.exists(f"{blog_file}"):
            print(f"错误：文件 '{blog_file}' 不存在")
            return {"success": False, "error": "文件不存在"}
        
        with open(f"{blog_file}", "r", encoding="utf-8") as f:
            original_text = f.read()
        
        # 2. 提取主题（从标题中）
        lines = original_text.split("\n")
        topic = "未命名博客"
        for line in lines:
            if line.startswith("# "):
                topic = line[2:].strip()
                break
        
        # 3. 润色博客内容
        print(f"正在润色博客 '{topic}'...")
        polished_text = self.text_processor.polish_text(original_text, "blog")
        
        # 4. 保存润色后的博客
        base_name = os.path.splitext(f"{blog_file}")[0]
        polished_blog_file = f"{base_name}_polished.md"
        
        with open(f"{polished_blog_file}", "w", encoding="utf-8") as f:
            f.write(polished_text)
        
        print(f"润色后的博客已保存至: {polished_blog_file}")
        
        # 5. 生成语音文件（如果需要）
        audio_file = None
        if with_tts:
            print("正在生成语音文件...")
            audio_file = f"{base_name}.wav"
            self.tts_service.text_to_speech(polished_text, audio_file)
        
        return {
            "topic": topic,
            "original_file": f"{blog_file}",
            "polished_file": f"{polished_blog_file}",
            "audio_file": f"{audio_file}" if audio_file else None,
            "success": True
        }


if __name__ == "__main__":
    # 初始化博客生成器
    blog_generator = BlogGenerator()
    
    # 示例：根据主题生成博客并添加语音
    topic = "AI 技术在医疗领域的应用"
    result = blog_generator.generate_blog(topic, with_tts=True)
    
    # 打印结果
    print(result)