"""
RFTKit - Reinforcement Fine-Tuning Toolkit

A comprehensive toolkit for OpenAI's Reinforcement Fine-Tuning (RFT), featuring:
- Pydantic-based grader creation
- Cluster-based rubric evaluation system
- Formatting, indicator, and rubric graders
- Multi-grader aggregation
"""

__version__ = "0.1.0"

from .types import GraderType, RubricItem, Message
from .base import BaseGrader, PythonGrader, ScoreModelGrader, MultiGrader, WeightedGrader
from .graders.formatting import FormattingGrader
from .graders.indicator import IndicatorGrader
from .graders.rubric import RubricGrader
from .graders.aggregator import AggregatorGrader
from .utils import (
    export_grader_config,
    load_grader_config,
    validate_grader_config,
    create_rubric_to_indicator_map,
    summarize_grader_config,
)

__all__ = [
    "GraderType",
    "RubricItem",
    "Message",
    "BaseGrader",
    "PythonGrader",
    "ScoreModelGrader",
    "MultiGrader",
    "WeightedGrader",
    "FormattingGrader",
    "IndicatorGrader",
    "RubricGrader",
    "AggregatorGrader",
    "export_grader_config",
    "load_grader_config",
    "validate_grader_config",
    "create_rubric_to_indicator_map",
    "summarize_grader_config",
]
