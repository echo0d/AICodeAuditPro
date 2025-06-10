# 初始化LLM
from typing import List

import networkx as nx

from core import C
from core.models import SourceFile, CodeUnit
from prompt import PROMPT_AGENT_1, PROMPT_AGENT_2
from utils import parse_code_uint, gen_graph_by_codeunits
from .llm_factory import llm_client

async def chat_completion_text(text:str,prompt:str):
    messages=[]
    messages.append({
        "role":"system",
        "content":prompt
    })
    messages.append({
        "role":"user",
        "content":text
    })
    res=await chat_completion_messages(messages)
    return res

async def chat_completion_messages(messages: list) -> str:
    return await llm_client.chat_completion(messages)

#负责解析项目依赖，生成项目依赖图谱
async def agent_1(sourceFile:SourceFile)->List[nx.Graph]:
    """
    使用语言模型解析代码中的依赖关系。

    :param sourceFile:
    :param code: 输入的 Python 代码字符串
    :return: 解析后的依赖关系描述字符串
    """
    response = await chat_completion_text(sourceFile.source_code,PROMPT_AGENT_1)
    #解析为对象数据
    res=parse_code_uint(code=sourceFile.source_code,path=sourceFile.path,name=sourceFile.name,input_text=response)
    return res

async def agent_2(text:str)->str:
    response = await chat_completion_text(text, PROMPT_AGENT_2)
    # 解析为对象数据
    return response