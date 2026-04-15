"""
RFTKit - Reinforcement Fine-Tuning Toolkit

A comprehensive toolkit for OpenAI's Reinforcement Fine-Tuning (RFT), featuring:
- Pydantic-based grader creation
- Graders API SDK
- Dataset utilities for RFT workflows
"""

__version__ = "0.1.0"

from .types import GraderType, RubricItem, Message
from .base import BaseGrader, PythonGrader, StringCheckGrader, TextSimilarityGrader, ScoreModelGrader, MultiGrader, WeightedGrader
from .graders.formatting import FormattingGrader
from .graders.rubric import RubricGrader
from .utils import (
    export_grader_config,
    load_grader_config,
    validate_grader_config,
    summarize_grader_config,
)

__all__ = [
    "GraderType",
    "RubricItem",
    "Message",
    "BaseGrader",
    "PythonGrader",
    "StringCheckGrader",
    "TextSimilarityGrader",
    "ScoreModelGrader",
    "MultiGrader",
    "WeightedGrader",
    "FormattingGrader",
    "RubricGrader",
    "export_grader_config",
    "load_grader_config",
    "validate_grader_config",
    "summarize_grader_config",
]
