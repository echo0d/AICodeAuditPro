# LLM工厂类，用于创建不同的LLM客户端
from typing import Any, Dict, List
from openai import AsyncOpenAI
from core import C

class BaseLLMClient:
    """基础LLM客户端抽象类"""
    
    def __init__(self, config):
        self.config = config
        self.client = self._create_client()
    
    def _create_client(self):
        """创建具体的客户端实例，子类需要重写此方法"""
        raise NotImplementedError
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """通用的聊天完成接口"""
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            raise Exception(f"No response from {self.__class__.__name__}")

class OpenAIClient(BaseLLMClient):
    """OpenAI客户端"""
    
    def _create_client(self):
        return AsyncOpenAI(
            base_url=self.config.base_url,
            api_key=self.config.api_key
        )

class AnthropicClient(BaseLLMClient):
    """Anthropic Claude客户端"""
    
    def _create_client(self):
        try:
            import anthropic
            return anthropic.AsyncAnthropic(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
        except ImportError:
            raise ImportError("请安装anthropic包: pip install anthropic")
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        # Claude需要特殊处理system消息
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
    
    def _create_client(self):
        # Azure需要特殊处理，需要endpoint和api_version字段
        endpoint = getattr(self.config, 'endpoint', None) or self.config.base_url
        api_version = getattr(self.config, 'api_version', '2024-02-15-preview')
        
        return AsyncOpenAI(
            api_key=self.config.api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )

class QwenClient(BaseLLMClient):
    """阿里通义千问客户端"""
    
    def _create_client(self):
        return AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

class GLMClient(BaseLLMClient):
    """智谱GLM客户端"""
    
    def _create_client(self):
        return AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

class DeepSeekClient(BaseLLMClient):
    """DeepSeek客户端"""
    
    def _create_client(self):
        return AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

class LLMFactory:
    """LLM工厂类"""
    
    # 注册所有支持的LLM提供商
    _PROVIDERS = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "azure": AzureClient,
        "qwen": QwenClient,
        "glm": GLMClient,
        "deepseek": DeepSeekClient,
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
        
        # 获取客户端类
        client_class = LLMFactory._PROVIDERS[provider]
        
        # 使用统一的llm配置
        return client_class(C.llm)
    
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
