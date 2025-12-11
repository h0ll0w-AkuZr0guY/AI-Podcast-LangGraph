# AI-Podcast-LangGraph

基于本地ollama的文本润色调整 + dashscope云端TTS的博客生成项目

## 功能介绍

1. **文本润色**：使用本地ollama模型或OpenAI API对输入文本进行智能润色，提升博客质量
2. **语音合成**：调用dashscope云端TTS API将文本转换为自然流畅的语音
3. **博客生成**：整合文本润色和语音合成功能，生成完整的博客内容和对应的语音文件

## 技术栈

- **Python**：项目开发语言
- **ollama**：本地大语言模型调用（默认使用）
- **OpenAI**：云端大语言模型调用（可选）
- **dashscope**：云端TTS服务
- **dotenv**：环境变量管理
- **requests**：HTTP请求处理

## 项目结构

```
AI-Podcast-LangGraph/
├── main.py                    # 主程序入口
├── src/
│   ├── __init__.py            # 初始化模块
│   ├── text_processing.py     # 文本润色处理
│   ├── tts_service.py         # TTS服务调用
│   └── blog_generator.py      # 博客生成逻辑
├── .env.sample                # 环境变量配置示例
├── requirements.txt           # 依赖列表
└── README.md                  # 项目说明文档
```

## 安装说明

1. **克隆项目**
   ```bash
   git clone git@github.com:h0ll0w-AkuZr0guY/AI-Podcast-LangGraph.git
   cd AI-Podcast-LangGraph
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   - 确保已安装本地ollama并启动服务
   - 编辑`.env.sample`文件，配置API密钥和其他参数
   ```bash
   cp .env.sample .env
   ```

## 使用方法

### 基本使用

运行主程序：

```bash
python main.py
```

根据提示输入博客内容或主题，系统将自动进行文本润色和语音合成。

### 功能模块

1. **文本润色**
   - 输入原始文本
   - 系统使用ollama模型进行智能润色
   - 输出润色后的高质量文本

2. **语音合成**
   - 输入文本内容
   - 调用modelscope API生成语音
   - 保存为音频文件

3. **完整博客生成**
   - 输入博客主题或大纲
   - 系统自动生成博客内容
   - 进行文本润色
   - 生成对应的语音文件

## 配置说明

### .env.sample文件配置

```env
# OpenAI Configuration or use Ollama，we use Ollama in this project
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_URL=http://localhost:11434/v1
OPENAI_MODEL=qwen2:0.5b

# Dashscope API Configuration
DASHSCOPE_API_KEY=your-dashscope-api-key
DASHSCOPE_MODEL=cosyvoice-v2
DASHSCOPE_VOICE=longxiaochun_v2
```

## 注意事项

1. **本地ollama服务**
   - 确保已安装ollama并启动服务：`ollama serve`
   - 确保已拉取所需模型：`ollama pull qwen2:0.5b`（或您配置的其他模型）

2. **API密钥**
   - 请妥善保管您的dashscope API密钥
   - 避免将API密钥提交到版本控制系统
   - 可使用`.env.example`作为模板创建`.env`文件

3. **网络连接**
   - 语音合成功能需要稳定的网络连接
   - 文本润色功能使用本地ollama时可离线使用，使用OpenAI API时需要网络连接

4. **输出文件**
   - 生成的语音文件默认保存为`output.mp3`
   - 生成的博客文本默认保存为`blog_时间戳.md`

## 扩展开发

### 添加新功能

1. **修改文本润色提示模板**：编辑`src/text_processing.py`中的提示词
2. **添加新的TTS语音类型**：修改`.env`文件中的`DASHSCOPE_VOICE`参数
3. **集成其他LLM模型**：修改`src/text_processing.py`中的模型调用逻辑
4. **更改TTS模型**：修改`.env`文件中的`DASHSCOPE_MODEL`参数

### 自定义输出格式

1. 修改`src/blog_generator.py`中的输出格式
2. 调整语音文件的保存路径和格式
3. 修改`src/tts_service.py`中的输出文件格式

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交Issue或Pull Request。
