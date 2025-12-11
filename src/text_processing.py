import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class TextProcessor:
    def __init__(self):
        try:
            self.client = OpenAI(base_url=os.getenv("OPENAI_API_URL"), api_key='ollama')
            self.model = os.getenv("OPENAI_MODEL", "qwen2:0.5b")
            self.client.models.list()
            print(f"Successfully connected to OLLM service, using model: {self.model}")
        except Exception as e:
            raise ConnectionError(f"LLM service connection failed: {e}")
    
    def polish_text(self, original_text: str, polish_type: str = "blog") -> str:
        """
        使用OpenAI模型对文本进行润色
        
        Args:
            original_text: 原始文本
            polish_type: 润色类型，可选值：blog, article, story等
            
        Returns:
            润色后的文本
        """
        # 设计润色提示模板
        messages = [
            {
                "role": "system",
                "content": f"你是一位专业的{polish_type}编辑，请将用户提供的文本润色为高质量内容。"
            },
            {
                "role": "user",
                "content": f"""请将以下文本润色为高质量的{polish_type}内容，要求：
1. 语言流畅自然，符合中文表达习惯
2. 逻辑清晰，结构合理
3. 用词准确，富有表现力
4. 保持原文核心意思不变
5. 提升文本的可读性和吸引力

原始文本：
{original_text}

润色后的文本：
"""
            }
        ]
        
        try:
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"文本润色失败: {str(e)}")
            return original_text
    
    def generate_blog_from_topic(self, topic: str, length: str = "medium") -> str:
        """
        根据主题生成博客内容
        
        Args:
            topic: 博客主题
            length: 博客长度，可选值：short, medium, long
            
        Returns:
            生成的博客内容
        """
        # 根据长度设置生成要求
        length_map = {
            "short": "约300字",
            "medium": "约500-800字",
            "long": "约1000字以上"
        }
        
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的博客作家，擅长根据主题生成高质量的博客内容。"
            },
            {
                "role": "user",
                "content": f"""
请根据以下主题生成一篇{length_map[length]}的高质量博客：

主题：{topic}

要求：
1. 语言流畅自然，符合中文表达习惯
2. 结构清晰，有标题、引言、正文和结论
3. 内容丰富，有深度和见解
4. 用词准确，富有表现力
5. 适合发布在博客平台

生成的博客：
"""
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"博客生成失败: {str(e)}")
            return f"无法生成关于'{topic}'的博客内容，请重试。"


if __name__ == "__main__":
    processor = TextProcessor()
    sample_text = "这是一篇关于AI技术的博客，探讨了最新的研究成果和应用场景。"
    polished_text = processor.polish_text(sample_text, polish_type="blog")
    print(polished_text)