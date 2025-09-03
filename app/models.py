from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class PromptParams(BaseModel):
    mandatory: List[str]
    optional: List[str]


class PromptMetadata(BaseModel):
    name: str
    code: int
    scope: str
    params: PromptParams
    file: str


class PromptTemplate(BaseModel):
    name: str
    code: int
    scope: str
    params: PromptParams
    content: str


class PromptListResponse(BaseModel):
    prompts: List[PromptMetadata]


class PromptResponse(BaseModel):
    prompt: PromptTemplate
