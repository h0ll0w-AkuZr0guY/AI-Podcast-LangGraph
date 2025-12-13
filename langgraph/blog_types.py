# 博客生成工作流的状态定义
from typing import TypedDict, Optional, List


class BlogConfig(TypedDict):
    """
    博客生成配置
    """
    topic: str  # 博客主题
    length: str  # 博客长度，可选值：short, medium, long
    with_tts: bool  # 是否生成语音文件
    polish_type: str  # 润色类型，可选值：blog, article, story等


class WorkflowState(TypedDict):
    """
    工作流状态
    """
    # 输入
    config: BlogConfig  # 博客生成配置
    original_text: Optional[str] = None  # 原始生成文本
    
    # 输出
    polished_text: Optional[str] = None  # 润色后文本
    blog_file: Optional[str] = None  # 博客文件路径
    audio_file: Optional[str] = None  # 音频文件路径（如果生成）
    error: Optional[str] = None  # 如果任何步骤失败，则为错误消息
    metadata: dict = {}  # 关于工作流的附加元数据
