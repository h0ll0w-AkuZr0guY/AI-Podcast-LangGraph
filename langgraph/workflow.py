from langgraph.graph import StateGraph, END
from src.text_processing import TextProcessor
from src.tts_service import TTSService
from src.blog_generator import BlogGenerator
from .blog_types import WorkflowState
from datetime import datetime
import os


class BlogWorkflow:
    """
    博客生成工作流
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.tts_service = TTSService()
        self.blog_generator = BlogGenerator()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """
        构建工作流
        """
        workflow = StateGraph(WorkflowState)
        
        # 添加节点
        workflow.add_node("generate_blog", self.generate_blog)
        workflow.add_node("polish_text", self.polish_text)
        workflow.add_node("save_blog", self.save_blog)
        workflow.add_node("generate_audio", self.generate_audio)
        
        # 添加边
        workflow.add_edge("generate_blog", "polish_text")
        workflow.add_edge("polish_text", "save_blog")
        workflow.add_conditional_edges(
            "save_blog",
            self._should_generate_audio,
            {
                True: "generate_audio",
                False: END
            }
        )
        workflow.add_edge("generate_audio", END)
        
        # 设置入口点
        workflow.set_entry_point("generate_blog")
        
        return workflow.compile()
    
    def generate_blog(self, state: WorkflowState) -> WorkflowState:
        """
        生成博客内容
        """
        try:
            config = state["config"]
            print(f"正在根据主题 '{config['topic']}' 生成博客内容...")
            
            # 生成原始博客内容
            original_text = self.text_processor.generate_blog_from_topic(
                config["topic"], config["length"]
            )
            
            return {
                **state,
                "original_text": original_text,
                "metadata": {**state["metadata"], "generated_at": datetime.now().isoformat()}
            }
        
        except Exception as e:
            error_msg = f"博客生成失败: {str(e)}"
            print(error_msg)
            return {
                **state,
                "error": error_msg
            }
    
    def polish_text(self, state: WorkflowState) -> WorkflowState:
        """
        润色博客内容
        """
        try:
            config = state["config"]
            print("正在润色博客内容...")
            
            # 润色博客内容
            polished_text = self.text_processor.polish_text(
                state["original_text"], config["polish_type"]
            )
            
            return {
                **state,
                "polished_text": polished_text,
                "metadata": {**state["metadata"], "polished_at": datetime.now().isoformat()}
            }
        
        except Exception as e:
            error_msg = f"文本润色失败: {str(e)}"
            print(error_msg)
            return {
                **state,
                "error": error_msg
            }
    
    def save_blog(self, state: WorkflowState) -> WorkflowState:
        """
        保存博客文本到文件
        """
        try:
            config = state["config"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            blog_file = f"results/blog_{timestamp}.md"
            
            # 确保results目录存在
            os.makedirs("results", exist_ok=True)
            
            # 保存博客文本
            with open(blog_file, "w", encoding="utf-8") as f:
                f.write(f"# {config['topic']}\n\n")
                f.write(state["polished_text"])
            
            print(f"博客文本已保存至: {blog_file}")
            
            return {
                **state,
                "blog_file": blog_file,
                "metadata": {**state["metadata"], "saved_at": datetime.now().isoformat()}
            }
        
        except Exception as e:
            error_msg = f"保存博客失败: {str(e)}"
            print(error_msg)
            return {
                **state,
                "error": error_msg
            }
    
    def generate_audio(self, state: WorkflowState) -> WorkflowState:
        """
        生成语音文件
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = f"results/audio_{timestamp}.mp3"
            
            print("正在生成语音文件...")
            
            # 生成语音文件
            success = self.tts_service.text_to_speech(
                state["polished_text"], audio_file
            )
            
            if success:
                print(f"语音合成成功，音频文件已保存至: {audio_file}")
                return {
                    **state,
                    "audio_file": audio_file,
                    "metadata": {**state["metadata"], "audio_generated_at": datetime.now().isoformat()}
                }
            else:
                error_msg = "语音合成失败"
                print(error_msg)
                return {
                    **state,
                    "error": error_msg
                }
        
        except Exception as e:
            error_msg = f"生成音频失败: {str(e)}"
            print(error_msg)
            return {
                **state,
                "error": error_msg
            }
    
    def _should_generate_audio(self, state: WorkflowState) -> bool:
        """
        判断是否需要生成音频
        """
        return state["config"]["with_tts"] and state["polished_text"] is not None
    
    def run(self, config: dict) -> WorkflowState:
        """
        运行工作流
        """
        # 确保results目录存在
        os.makedirs("results", exist_ok=True)
        
        # 执行工作流
        initial_state: WorkflowState = {
            "config": config,
            "metadata": {"workflow_started_at": datetime.now().isoformat()}
        }
        
        result = self.workflow.invoke(initial_state)
        return result
