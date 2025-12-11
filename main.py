from src.blog_generator import BlogGenerator

def display_menu():
    """
    显示主菜单
    """
    print("=" * 50)
    print("AI 博客生成与语音合成系统")
    print("=" * 50)
    print("1. 根据主题生成完整博客（带语音）")
    print("2. 仅生成博客文本（不生成语音）")
    print("3. 对已有文本进行润色和语音生成")
    print("4. 处理已有的博客文件")
    print("5. 退出程序")
    print("=" * 50)

def get_valid_choice(prompt: str, min_val: int, max_val: int) -> int:
    """
    获取有效的用户选择
    
    Args:
        prompt: 提示信息
        min_val: 最小值
        max_val: 最大值
        
    Returns:
        有效的用户选择
    """
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"请输入 {min_val} 到 {max_val} 之间的数字")
        except ValueError:
            print("请输入有效的数字")

def get_blog_length() -> str:
    """
    获取博客长度选择
    
    Returns:
        博客长度（short/medium/long）
    """
    print("请选择博客长度：")
    print("1. 短（约300字）")
    print("2. 中（约500-800字）")
    print("3. 长（约1000字以上）")
    
    length_map = {
        1: "short",
        2: "medium",
        3: "long"
    }
    choice = get_valid_choice("请输入选择：", 1, 3)
    return length_map[choice]

def main():
    """
    主程序入口
    """
    # 初始化博客生成器
    blog_generator = BlogGenerator()
    
    while True:
        # 显示菜单
        display_menu()
        
        # 获取用户选择
        choice = get_valid_choice("请输入选择：", 1, 5)
        
        if choice == 1:
            # 1. 根据主题生成完整博客（带语音）
            topic = input("请输入博客主题：")
            length = get_blog_length()
            
            print("=" * 50)
            result = blog_generator.generate_blog(topic, length, with_tts=True)
            print("=" * 50)
            print("博客生成完成！")
            print(f"主题：{result['topic']}")
            print(f"博客文件：{result['blog_file']}")
            print(f"音频文件：{result['audio_file']}")
            print("=" * 50)
            
        elif choice == 2:
            # 2. 仅生成博客文本（不生成语音）
            topic = input("请输入博客主题：")
            length = get_blog_length()
            
            print("=" * 50)
            result = blog_generator.generate_blog(topic, length, with_tts=False)
            print("=" * 50)
            print("博客文本生成完成！")
            print(f"主题：{result['topic']}")
            print(f"博客文件：{result['blog_file']}")
            print("=" * 50)
            
        elif choice == 3:
            # 3. 对已有文本进行润色和语音生成
            print("请输入要润色的文本（输入 'EOF' 结束）：")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'EOF':
                    break
                lines.append(line)
            
            original_text = '\n'.join(lines)
            if not original_text.strip():
                print("错误：输入文本不能为空")
                continue
            
            print("请选择润色类型：")
            print("1. 博客")
            print("2. 文章")
            print("3. 故事")
            print("4. 其他")
            
            type_map = {
                1: "blog",
                2: "article",
                3: "story",
                4: "other"
            }
            
            type_choice = get_valid_choice("请输入选择：", 1, 4)
            polish_type = type_map[type_choice]
            
            print("=" * 50)
            result = blog_generator.polish_and_tts(original_text, polish_type)
            print("=" * 50)
            if result['success']:
                print("文本润色和语音生成完成！")
                print(f"音频文件：{result['audio_file']}")
            else:
                print("处理失败，请重试")
            print("=" * 50)
            
        elif choice == 4:
            # 4. 处理已有的博客文件
            blog_file = input("请输入博客文件路径：")
            
            print("是否生成语音文件？")
            print("1. 是")
            print("2. 否")
            
            tts_choice = get_valid_choice("请输入选择：", 1, 2)
            with_tts = tts_choice == 1
            
            print("=" * 50)
            result = blog_generator.process_existing_blog(blog_file, with_tts)
            print("=" * 50)
            if result['success']:
                print("博客文件处理完成！")
                print(f"主题：{result['topic']}")
                print(f"原始文件：{result['original_file']}")
                print(f"润色后文件：{result['polished_file']}")
                if result['audio_file']:
                    print(f"音频文件：{result['audio_file']}")
            else:
                print(f"处理失败：{result.get('error', '未知错误')}")
            print("=" * 50)
            
        elif choice == 5:
            # 5. 退出程序
            print("感谢使用 AI 博客生成与语音合成系统！")
            break
        
        # 询问用户是否继续
        input("\n按 Enter 键继续...")

if __name__ == "__main__":
    main()
