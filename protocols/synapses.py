from typing import Optional, List, Dict
import bittensor as bt
from pydantic import BaseModel

from protocols.llm_engine import QueryOutput

# protocol version
VERSION = 5
ERROR_TYPE = int


# Default settings for miners
MAX_MINER_INSTANCE = 9


class DiscoveryMetadata(BaseModel):
    network: str = None


class DiscoveryOutput(BaseModel):
    metadata: DiscoveryMetadata = None
    block_height: int = None
    start_block_height: int = None
    balance_model_last_block: int = None
    run_id: str = None
    version: Optional[int] = VERSION


class BaseSynapse(bt.Synapse):
    version: int = VERSION


class Discovery(BaseSynapse):
    output: DiscoveryOutput = None
                        
    def deserialize(self):
        return self


class GenericQueryOutput(BaseModel):
    result: Optional[List[Dict]] = None    
    error: Optional[ERROR_TYPE] = None


class Query(BaseSynapse):
    network: str = None
    type: str = None

    # search query
    target: str = None
    where: Optional[Dict] = None
    limit: Optional[int] = None
    skip: Optional[int] = 0

    # output
    output: Optional[QueryOutput] = None

    def deserialize(self) -> Dict:
        return self.output


class Benchmark(BaseSynapse):
    network: str = None
    query: str = None

    # output
    output: Optional[float] = None

    def deserialize(self) -> Dict:
        return self.output


class Challenge(BaseSynapse):
    model_type: str # model type

    # For BTC funds flow model
    in_total_amount: Optional[int] = None
    out_total_amount: Optional[int] = None
    tx_id_last_4_chars: Optional[str] = None
    
    # For BTC balance tracking model
    block_height: Optional[int] = None
    
    # Altcoins
    checksum: Optional[str] = None

    output: Optional[str] = None
    
    def deserialize(self) -> str:
        return self.output


class LlmMessage(BaseModel):
    type: int = None
    content: str = None


class LlmQuery(BaseSynapse):
    network: str = None    
    # decide whether to invoke a generic llm endpoint or not
    # is_generic_llm: bool = False  
    # messages: conversation history for llm agent to use as context
    messages: List[LlmMessage] = None

    # output
    output: Optional[QueryOutput] = None
    def deserialize(self) -> str:
        return self.output


class GenericLlmQuery(BaseSynapse):
    is_generic_llm: bool = True
    messages: List[LlmMessage] = None

    # output
    output: Optional[GenericQueryOutput] = None
    def deserialize(self) -> str:
        return self.output
