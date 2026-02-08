from abc import ABC, abstractmethod
from typing import Any


class FieldExtractor(ABC):
    """Abstract base class for field-specific extractors."""

    @abstractmethod
    def extract(self, text: str) -> Any:
        """Extract the specific field from raw text."""
        pass

