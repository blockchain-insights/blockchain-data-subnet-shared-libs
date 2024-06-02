from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from protocols.llm_engine import QueryOutput


class ChatMessageRequest(BaseModel):
    network: str = Field(..., description="network name")
    prompt: str = Field(..., description="user prompt")


class ChatMessageVariantRequest(BaseModel):
    network: str = Field(..., description="network name")
    prompt: str = Field(..., description="user prompt")
    miner_hotkey: str = Field(..., description="miner hotkey")


class ChatMessageResponse(BaseModel):
    miner_hotkey: Optional[str] = Field(None, description="miner hotkey")
    response: List[QueryOutput] = Field(..., description="response from llm engine")


class ContentType(str, Enum):
    text = "text"
    graph = "graph"
    table = "table"


