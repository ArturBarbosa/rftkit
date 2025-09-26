"""Core types for OpenAI's Reinforcement Fine-Tuning graders."""

from enum import Enum
from typing import Literal, TypedDict


class GraderType(Enum):
    """
    Grader types defined by OpenAI's RFT API.
    
    References:
        https://platform.openai.com/docs/guides/graders
    """
    SCORE_MODEL = "score_model"
    LABEL_MODEL = "label_model"
    PYTHON = "python"
    MULTI = "multi"
    STRING_CHECK = "string_check"
    TEXT_SIMILARITY = "text_similarity"


class RubricItem(TypedDict):
    """Rubric item for evaluation criteria."""
    id: int
    content: str


class Message(TypedDict):
    """Message structure for chat-based graders."""
    role: Literal["user", "system", "assistant", "developer"]
    content: str

