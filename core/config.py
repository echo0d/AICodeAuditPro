from loguru import logger
import os
import yaml

from .models import Config

def load_yaml_as_pydantic(file_path: str, model_cls) -> Config:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = yaml.safe_load(file)
    return model_cls(**data)

def create_default_config(file_path):
    """创建默认配置文件"""
    default_config = {
        'llm': {
            'provider': 'openai'
        },
        'openai': {
            'base_url': 'https://api.openai-proxy.org/v1',
            'api_key': "sk-BKR5huAmRgTd1qjwP6AWocZXvmgTjJ2UI46uiHi104YT4Jnh",
            'model': 'gpt-4o-mini',
            'max_tokens': 4000
        },
        'anthropic': {
            'api_key': '',
            'base_url': 'https://api.anthropic.com',
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 4000
        },
        'azure': {
            'api_key': '',
            'endpoint': '',
            'api_version': '2024-02-15-preview',
            'model': 'gpt-4o-mini',
            'max_tokens': 4000
        },
        'qwen': {
            'api_key': '',
            'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
            'model': 'qwen-plus',
            'max_tokens': 2000
        },
        'glm': {
            'api_key': '',
            'base_url': 'https://open.bigmodel.cn/api/paas/v4',
            'model': 'glm-4',
            'max_tokens': 4000
        },
        'deepseek': {
            'api_key': '',
            'base_url': 'https://api.deepseek.com',
            'model': 'deepseek-chat',
            'max_tokens': 4000
        },
        'project': {
            "source_file_ext": [".py", ".go", ".js", ".java", ".cpp", ".php", ".aspx", ".asp", ".c", ".cs"],
            "config_file_ext": [".yaml", ".xml", ".json", ".conf", ".ini", ".toml", ".config", ".settings"],
            "exclude_dir": ['node_modules', "dist", "build", "out", "venv", ".venv", "env", "target", "vendor",
                          "bower_components",
                          ".git", ".svn", ".hg", ".idea", ".vscode", ".metadata", "nbproject", "test", "tests", "spec",
                          "specs",
                          "tmp", "temp", "cache", "logs", "docker", "containers", "k8s", "kube", ".circleci", ".github",
                          ".travis", "docs", "doc", ".secrets", ".env"],
            "exclude_max_file_size": 1
        }
    }
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(default_config, file, default_flow_style=False)
    logger.info(f"已创建默认配置文件: {file_path}")

def load_or_create_config(yaml_path):
    """加载或创建配置文件"""
    if not os.path.exists(yaml_path):
        logger.info(f"配置文件未找到: {yaml_path}")
        create_default_config(yaml_path)
    config = load_yaml_as_pydantic(yaml_path, Config)
    return config
