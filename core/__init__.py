# Core module - 整合了配置和模型定义
from .models import (
    SourceFile, SourceDir, LLMConfig, OpenAIConfig, AnthropicConfig, 
    AzureConfig, QwenConfig, GLMConfig, DeepSeekConfig, ProjectConfig, 
    Config, CodeUnit
)
from .config import load_or_create_config

# 全局配置实例
C = load_or_create_config('config.yaml')

__all__ = [
    'SourceFile', 'SourceDir', 'LLMConfig', 'OpenAIConfig', 'AnthropicConfig',
    'AzureConfig', 'QwenConfig', 'GLMConfig', 'DeepSeekConfig', 'ProjectConfig',
    'Config', 'CodeUnit', 'load_or_create_config', 'C'
]
