import os
from typing import List, Optional
from google import genai
from pydantic import BaseModel

from resume_parser_framework.extractor.extractor_base import FieldExtractor


class SkillsSchema(BaseModel):
    skills: List[str]

class SkillsExtractorLLM(FieldExtractor):
    """
    Skills extraction with Gemini
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
    ):
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY was not found")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.system_prompt = (
            """You are a high-precision resume parser.
               Extract only hard skills, technical frameworks, and professional certifications.
               Strictly exclude generic soft skills such as 'leadership' or 'communication' 
               unless they are tied to a specific professional methodology."""
        )

    def extract(self, text: str) -> List[str]:
        if not text.strip():
            return []
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"Extract skills from this CV: {text[:4000]}",
                config={
                    "system_instruction": self.system_prompt,
                    "response_mime_type": "application/json",
                    "response_schema": SkillsSchema, 
                    "temperature": 0.1,
                }
            )

            extracted_data = response.parsed
            return sorted(list(set(extracted_data.skills)))

        except Exception as e:
            raise RuntimeError("LLM skill extraction failed") from e

