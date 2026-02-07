from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ResumeData:
    """Structured resume information."""
    name: str | None = None
    email: str | None = None
    skills: List[str] = field(default_factory=list)

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "skills": self.skills,
        }