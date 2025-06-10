# AI Code Audit Pro

基于https://github.com/xy200303/AiCodeAudit项目改进

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/echo0d/AICodeAuditPro.git
cd AICodeAuditPro
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行参数

```bash
python main.py -d <target_dir> -o <output_dir> -b <batch_size>
```

参数说明：
- `-d`：目标项目目录路径（默认："./演示项目/openssh-9.9p1"）
- `-o`：输出文件目录（默认："./output"）
- `-b`：并发处理数量（默认：100）

### 示例

```bash
# 使用默认参数审计示例项目
python main.py

# 指定目标目录和输出目录
python main.py -d ./your-project -o ./audit-results

# 调整并发数量
python main.py -d ./your-project -b 50
```

## 输出结果

审计完成后，在输出目录中会生成以下文件：
- `<project_md5>.graphml`：项目依赖关系图
- `<project_md5>_审计结果.log`：详细的审计报告

项目依赖关系图可以用`PyVis.py`生成为`html`文件

## 配置文件

项目配置在`config.yaml`文件中，可以根据需要调整相关参数。

支持的LLM提供商

1. **OpenAI** (默认)
2. **Anthropic Claude**
3. **Azure OpenAI**
4. **阿里通义千问 (Qwen)**
5. **智谱GLM**
6. **DeepSeek**

### 配置方式

在 `config.yaml` 文件中，设置 `llm.provider` 字段来选择要使用的LLM：

```yaml
llm:
  provider: openai  # 可选: openai, anthropic, azure, qwen, glm, deepseek
```

然后配置对应的API密钥和参数。


### 安装额外依赖

根据您选择的LLM提供商，可能需要安装额外的依赖包：如果使用 Anthropic Claude

```bash
pip install anthropic
```

## 注意事项

1. 每个LLM提供商的API调用格式可能略有不同，但本项目已经封装了这些差异
2. 不同的模型可能有不同的token限制和定价
3. 建议在生产环境中使用环境变量来管理API密钥，而不是直接写在配置文件中

