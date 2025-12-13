#!/usr/bin/env python3
"""
使用LangGraph工作流生成博客和语音
"""

from langgraph.workflow import BlogWorkflow


def main():
    """
    主函数
    """
    # 示例配置
    config = {
        "topic": "AI技术在教育领域的应用",
        "length": "medium",
        "with_tts": True,
        "polish_type": "blog"
    }
    
    print("=" * 50)
    print("使用LangGraph工作流生成博客和语音")
    print("=" * 50)
    print(f"主题: {config['topic']}")
    print(f"长度: {config['length']}")
    print(f"生成语音: {config['with_tts']}")
    print(f"润色类型: {config['polish_type']}")
    print("=" * 50)
    
    # 创建工作流实例
    workflow = BlogWorkflow()
    
    # 执行工作流
    result = workflow.run(config)
    
    print("\n" + "=" * 50)
    print("工作流执行结果")
    print("=" * 50)
    
    if result.get("error"):
        print(f"❌ 执行失败: {result['error']}")
    else:
        print(f"✅ 执行成功")
        print(f"📝 博客文件: {result['blog_file']}")
        if result.get("audio_file"):
            print(f"🎵 音频文件: {result['audio_file']}")
        print(f"📊 元数据: {result['metadata']}")
    
    print("\n" + "=" * 50)
    print("工作流执行完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
