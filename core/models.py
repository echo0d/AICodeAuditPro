from pydantic import BaseModel, Field
from typing import List, Optional

class SourceFile(BaseModel):
    path: str
    name: str
    source_code: str
    extension: str

class SourceDir(BaseModel):
    path: str
    name: str
    source_dirs: Optional[List['SourceDir']] = Field(default_factory=list)
    source_files: Optional[List[SourceFile]] = Field(default_factory=list)

class LLMConfig(BaseModel):
    provider: str

class OpenAIConfig(BaseModel):
    api_key: str
    base_url: str
    max_tokens: int
    model: str

class AnthropicConfig(BaseModel):
    api_key: str
    base_url: str
    max_tokens: int
    model: str

class AzureConfig(BaseModel):
    api_key: str
    endpoint: str
    api_version: str
    max_tokens: int
    model: str

class QwenConfig(BaseModel):
    api_key: str
    base_url: str
    max_tokens: int
    model: str

class GLMConfig(BaseModel):
    api_key: str
    base_url: str
    max_tokens: int
    model: str

class DeepSeekConfig(BaseModel):
    api_key: str
    base_url: str
    max_tokens: int
    model: str

class ProjectConfig(BaseModel):
    config_file_ext: List[str] = []
    exclude_dir: List[str] = []
    exclude_max_file_size: float
    source_file_ext: List[str] = []

class Config(BaseModel):
    llm: LLMConfig
    openai: Optional[OpenAIConfig] = None
    anthropic: Optional[AnthropicConfig] = None
    azure: Optional[AzureConfig] = None
    qwen: Optional[QwenConfig] = None
    glm: Optional[GLMConfig] = None
    deepseek: Optional[DeepSeekConfig] = None
    project: ProjectConfig

class CodeUnit(BaseModel):
    source_code: str
    start_code_line: int
    end_code_line: int
    name: str
    path: str
    source_name: str
    target_name: str
    source_desc: str
