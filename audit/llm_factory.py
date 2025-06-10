# LLM工厂类，用于创建不同的LLM客户端
from typing import Any, Dict, List
from openai import AsyncOpenAI
from core import C

class BaseLLMClient:
    """基础LLM客户端抽象类"""
    
    def __init__(self, config):
        self.config = config
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """聊天完成接口"""
        raise NotImplementedError

class OpenAIClient(BaseLLMClient):
    """OpenAI客户端"""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = AsyncOpenAI(
            base_url=config.base_url,
            api_key=config.api_key
        )
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            raise Exception("No response from OpenAI")

class AnthropicClient(BaseLLMClient):
    """Anthropic Claude客户端"""
    def __init__(self, config):
        super().__init__(config)
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(
                api_key=config.api_key,
                base_url=config.base_url
            )
        except ImportError:
            raise ImportError("请安装anthropic包: pip install anthropic")
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        # 转换消息格式，Claude需要特殊处理system消息
        system_message = None
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)
        response = await self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=system_message,
            messages=user_messages
        )
        return response.content[0].text

class AzureClient(BaseLLMClient):
    """Azure OpenAI客户端"""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            api_version=config.api_version,
            azure_endpoint=config.endpoint
        )
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            raise Exception("No response from Azure OpenAI")

class QwenClient(BaseLLMClient):
    """阿里通义千问客户端"""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            raise Exception("No response from Qwen")

class GLMClient(BaseLLMClient):
    """智谱GLM客户端"""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:        
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            raise Exception("No response from GLM")

class DeepSeekClient(BaseLLMClient):
    """DeepSeek客户端"""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            raise Exception("No response from DeepSeek")

class LLMFactory:
    """LLM工厂类"""
    
    # 注册所有支持的LLM提供商
    _PROVIDERS = {
        "openai": (OpenAIClient, "openai"),
        "anthropic": (AnthropicClient, "anthropic"),
        "azure": (AzureClient, "azure"),
        "qwen": (QwenClient, "qwen"),
        "glm": (GLMClient, "glm"),
        "deepseek": (DeepSeekClient, "deepseek"),
    }
    
    @staticmethod
    def create_client(provider: str = None) -> BaseLLMClient:
        """根据配置创建对应的LLM客户端"""
        if provider is None:
            provider = C.llm.provider
        
        provider = provider.lower()
        
        # 检查是否支持该提供商
        if provider not in LLMFactory._PROVIDERS:
            supported = ", ".join(LLMFactory._PROVIDERS.keys())
            raise ValueError(f"不支持的LLM提供商: {provider}。支持的提供商: {supported}")
        
        # 获取客户端类和配置属性名
        client_class, config_attr = LLMFactory._PROVIDERS[provider]
        
        # 获取配置
        config = getattr(C, config_attr, None)
        if config is None:
            raise ValueError(f"{provider.upper()}配置未找到，请在config.yaml中配置{config_attr}部分")
        
        # 创建并返回客户端实例
        return client_class(config)
    
    @classmethod
    def get_supported_providers(cls) -> List[str]:
        """获取所有支持的LLM提供商列表"""
        return list(cls._PROVIDERS.keys())
    
    @classmethod
    def is_provider_supported(cls, provider: str) -> bool:
        """检查是否支持指定的LLM提供商"""
        return provider.lower() in cls._PROVIDERS

# 全局LLM客户端实例
llm_client = LLMFactory.create_client()
