from .workflow import BlogWorkflow


def main():
    """
    LangGraph博客生成工作流主入口
    """
    print("=" * 50)
    print("LangGraph 博客生成与语音合成系统")
    print("=" * 50)
    
    # 获取用户输入
    topic = input("请输入博客主题：")
    
    print("\n请选择博客长度：")
    print("1. 短（约300字）")
    print("2. 中（约500-800字）")
    print("3. 长（约1000字以上）")
    length_choice = input("请输入选择：")
    
    length_map = {
        "1": "short",
        "2": "medium",
        "3": "long"
    }
    length = length_map.get(length_choice, "medium")
    
    with_tts = input("\n是否生成语音文件？(y/n): ").lower() == "y"
    
    print("\n请选择润色类型：")
    print("1. 博客")
    print("2. 文章")
    print("3. 故事")
    print("4. 其他")
    polish_choice = input("请输入选择：")
    
    polish_map = {
        "1": "blog",
        "2": "article",
        "3": "story",
        "4": "other"
    }
    polish_type = polish_map.get(polish_choice, "blog")
    
    # 准备工作流配置
    config = {
        "topic": topic,
        "length": length,
        "with_tts": with_tts,
        "polish_type": polish_type
    }
    
    print("\n" + "=" * 50)
    print("开始执行工作流...")
    print("=" * 50)
    
    # 执行工作流
    workflow = BlogWorkflow()
    result = workflow.run(config)
    
    print("\n" + "=" * 50)
    print("工作流执行完成！")
    print("=" * 50)
    
    # 输出结果
    if result.get("error"):
        print(f"错误信息：{result['error']}")
    else:
        print(f"主题：{result['config']['topic']}")
        print(f"博客文件：{result['blog_file']}")
        if result.get("audio_file"):
            print(f"音频文件：{result['audio_file']}")
        print(f"执行时间：{result['metadata'].get('workflow_started_at')} - {result['metadata'].get('audio_generated_at', result['metadata'].get('saved_at'))}")
    
    print("\n感谢使用 LangGraph 博客生成与语音合成系统！")


if __name__ == "__main__":
    main()
