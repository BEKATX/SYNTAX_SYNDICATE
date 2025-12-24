from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ProviderResponse:
    content: str
    status: str  # "success" or "error"

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> ProviderResponse:
        pass