import re
import spacy


from abc import ABC, abstractmethod
from typing import Optional, Any, List


class FieldExtractor(ABC):
    """Abstract base class for field-specific extractors."""

    @abstractmethod
    def extract(self, text: str) -> Any:
        """Extract the specific field from raw text."""
        pass


class EmailExtractor(FieldExtractor):
    """Extracts email using regex (very reliable)."""

    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def extract(self, text: str) -> Optional[str]:
        match = self.EMAIL_REGEX.search(text)
        return match.group(0) if match else None


class NameExtractor(FieldExtractor):
    """Uses spaCy NER (ML-based) primarily.
    Falls back to first plausible name line, skipping common PDF junk like 'mpf'.
    """

    JUNK_LINES = {'mpf', 'footer', 'header', 'page', ''}

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise ImportError("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    

    def _clean_name_line(self, line: str) -> str:
        """Remove trailing emails, URLs, and common social links from a line."""
        line = re.split(r'\||@|https?://', line)[0]
        return line.strip()


    def extract(self, text: str) -> Optional[str]:
        if not text:
            return None

        header_text = text[:1200]

        header_text = re.sub(
            r'(?i)(curriculum vitae|resume|cv|\n+linkedin|\n+github|\n+portfolio|[\w\.-]+@[\w\.-]+).*', '',
            header_text, flags=re.DOTALL
            )
        
        doc = self.nlp(header_text)
        persons = [ent.text.strip().replace('\n', ' ') for ent in doc.ents if ent.label_ == "PERSON"]

        if persons:
            best = max(persons, key=lambda x: (len(x), x.count(' ')))
            if len(best.split()) >= 2:
                return best

        lines = [line.strip() for line in text.splitlines() if line.strip()][:8]

        for raw_line in lines:
            line = self._clean_name_line(raw_line)
            if line.lower() in self.JUNK_LINES:
                continue

            words = line.split()
            if (len(words) >= 2 and
                sum(1 for w in words if w and w[0].isupper()) >= len(words) * 0.7):
                return line
       
        non_junk_lines = [self._clean_name_line(line) for line in lines if line.lower() not in self.JUNK_LINES]
        if len(non_junk_lines) >= 2:
            return non_junk_lines[1]

        if lines:
            return lines[0]

        return None

class SkillsExtractor(FieldExtractor):
    """Keyword-based skills extraction, fixed to avoid substring conflicts."""

    COMMON_SKILLS = {
        "python", "java", "javascript", "react", "angular", "node", "sql",
        "machine learning", "deep learning", "llm", "nlp", "aws", "azure",
        "docker", "kubernetes", "git", "agile", "scrum"
    }

    def extract(self, text: str) -> List[str]:
        found = set()
        text_lower = text.lower()

        for skill in sorted(self.COMMON_SKILLS, key=len, reverse=True):
            skill_lower = skill.lower()
            if skill_lower in text_lower:
                idx = text_lower.find(skill_lower)
                original = text[idx : idx + len(skill_lower)]
                found.add(original)            
                text_lower = text_lower[:idx] + " " * len(skill_lower) + text_lower[idx+len(skill_lower):]

        return sorted(list(found))