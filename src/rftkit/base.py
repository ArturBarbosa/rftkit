"""Base classes for OpenAI Reinforcement Fine-Tuning graders."""

from abc import ABC, abstractmethod
from typing import Any, List
import importlib
import inspect

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from .types import Message, GraderType
from .constants import (
    DEFAULT_SAMPLING_PARAMS,
    DEFAULT_IMAGE_TAG,
    DEFAULT_WEIGHTED_GRADER_WEIGHT,
    DEFAULT_SCORE_MODEL,
    DEFAULT_SCORE_RANGE,
    DEFAULT_PASS_THRESHOLD,
    DEFAULT_SCORE_INPUT,
)


class BaseGrader(BaseModel, ABC):
    """
    Abstract base class for all OpenAI Reinforcement Fine-Tuning (RFT) graders.

    This class provides the foundation for all grader types used in OpenAI's RFT system.
    Each grader is responsible for evaluating model outputs according to specific criteria
    and returning a score that can be used for reinforcement learning.

    Attributes:
        name (str): Unique identifier for the grader instance

    References:
        OpenAI RFT Graders Documentation: https://platform.openai.com/docs/guides/graders

    Note:
        This is an abstract class and cannot be instantiated directly. Use one of the
        concrete grader implementations like PythonGrader or ScoreModelGrader.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., description="Name of the grader")

    def __init__(self, name: str, **kwargs):
        """
        Initialize a grader instance.

        Args:
            name (str): Unique identifier for this grader
        """
        super().__init__(name=name, **kwargs)

    @property
    @abstractmethod
    def config(self) -> dict[str, Any]:
        """
        Convert this grader to OpenAI's expected format for RFT API calls.

        Returns:
            dict[str, Any]: Dictionary representation compatible with OpenAI's RFT API
        """
        raise NotImplementedError("Subclasses must implement config property")


class PythonGrader(BaseGrader):
    """
    Base class for Python-based graders that execute custom Python code.

    Python graders allow you to implement custom grading logic using Python code
    that runs in a sandboxed environment. They are ideal for deterministic scoring
    rules, format validation, and complex logic that doesn't require LLM inference.

    The grader automatically loads Python source code from the grader_code module
    and packages it for execution in OpenAI's RFT environment.

    Examples:
        >>> grader = PythonGrader("format_checker", module_path="my_module.validator")
        >>> grader_config = grader.config
        >>> print(grader_config["type"])  # "python"

    Attributes:
        module_path (str): Python module path containing the grading logic
    """
    module_path: str = Field(..., description="Python source code module path")

    def process_code(self, code_str: str) -> str:
        """
        Optional method to process/transform the source code before including it in the config.
        Override this method in subclasses if you need to modify the code.

        Args:
            code_str: The raw source code string

        Returns:
            The processed source code string
        """
        return code_str

    @property
    def config(self) -> dict[str, Any]:
        grader_module = importlib.import_module(self.module_path)
        return {
            "name": self.name,
            "type": GraderType.PYTHON.value,
            "source": self.process_code(inspect.getsource(grader_module)),
            "image_tag": DEFAULT_IMAGE_TAG
        }


class ScoreModelGrader(BaseGrader):
    """
    Grader that uses Large Language Models to assign numerical scores to responses.

    Score model graders leverage the reasoning capabilities of LLMs to evaluate
    responses against complex criteria that may be difficult to encode in Python.
    They are particularly useful for assessing subjective qualities like creativity,
    coherence, or domain-specific expertise.

    The grader sends a structured prompt to the specified model and expects a
    numerical score within the defined range. The score is then normalized and
    compared against the pass threshold for binary classification.

    Attributes:
        input (List[Message]): Conversation messages that form the grading prompt
        model (str): OpenAI model identifier (e.g., "gpt-4", "gpt-4o")
        pass_threshold (float): Minimum score required for a "pass" classification
        range (list[float]): Two-element list [min_score, max_score] defining valid range
        sampling_params (dict[str, Any]): Model inference parameters for reproducibility

    Examples:
        >>> messages = [{"role": "user", "content": "Rate this essay from 1 to 5..."}]
        >>> grader = ScoreModelGrader(
        ...     name="essay_scorer",
        ...     model="gpt-4o",
        ...     input=messages,
        ...     pass_threshold=3,
        ...     range=[1, 5],
        ...     sampling_params={"temperature": 0.1}
        ... )
        >>> config = grader.config
    """

    input: List[Message] = Field(
        default_factory=lambda: DEFAULT_SCORE_INPUT.copy(),
        description="Input to the score model"
    )
    model: str = Field(
        default=DEFAULT_SCORE_MODEL,
        description="Model to use for scoring"
    )
    pass_threshold: float = Field(
        default=DEFAULT_PASS_THRESHOLD,
        description="Threshold for passing score"
    )
    range: list[float] = Field(
        default_factory=lambda: DEFAULT_SCORE_RANGE.copy(),
        description="Score range [min, max]"
    )
    sampling_params: dict[str, Any] = Field(
        default_factory=lambda: DEFAULT_SAMPLING_PARAMS.copy(),
        description="Sampling parameters for the model"
    )

    @field_validator('range')
    @classmethod
    def validate_range(cls, v: list[float]) -> list[float]:
        """Validate that range contains exactly 2 elements with min < max."""
        if len(v) != 2:
            raise ValueError("Range must contain exactly 2 elements: [min, max]")
        if v[0] >= v[1]:
            raise ValueError("Range minimum must be less than maximum")
        return v

    @model_validator(mode='after')
    def validate_pass_threshold_in_range(self) -> 'ScoreModelGrader':
        """Validate that pass_threshold is within the specified range."""
        if not (self.range[0] <= self.pass_threshold <= self.range[1]):
            raise ValueError(
                f"Pass threshold {self.pass_threshold} must be within range {self.range}"
            )
        return self

    @property
    def config(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": GraderType.SCORE_MODEL.value,
            "model": self.model,
            "input": self.input,
            "pass_threshold": self.pass_threshold,
            "range": self.range,
            "sampling_params": self.sampling_params
        }


class MultiGrader(BaseGrader):
    """
    Grader that combines multiple graders using a custom formula.

    MultiGrader allows you to aggregate the outputs of multiple graders
    (Python, ScoreModel, or other MultiGraders) using a custom calculation formula.
    This is useful for creating complex evaluation criteria that combine
    multiple aspects of quality.

    Attributes:
        graders (List[BaseGrader]): List of graders to combine

    Examples:
        >>> format_grader = PythonGrader("format", module_path="...")
        >>> content_grader = ScoreModelGrader("content", ...)
        >>> multi = MultiGrader(
        ...     name="combined",
        ...     graders=[format_grader, content_grader]
        ... )
    """
    graders: List[BaseGrader] = Field(..., description="List of graders to use")

    @property
    def graders_dict(self) -> dict[str, BaseGrader]:
        """
        Convert a list of graders to a dictionary keyed by name.
        
        Returns:
            dict[str, BaseGrader]: Dictionary mapping grader names to grader instances
        """
        return {grader.name: grader for grader in self.graders}

    @abstractmethod
    def _calculate_output(self) -> str:
        """
        Calculate the output formula for combining grader scores.
        
        Must return a string formula that references grader names.
        Example: "grader1 * 0.5 + grader2 * 0.5"
        """
        raise NotImplementedError("Subclasses must implement _calculate_output method")

    @property
    def config(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": GraderType.MULTI.value,
            "calculate_output": self._calculate_output(),
            "graders": {grader.name: grader.config for grader in self.graders},
        }


class WeightedGrader(BaseModel):
    """
    Mixin class for graders that have an associated weight.

    This is used for combining multiple graders where each grader
    contributes differently to the final score.

    Attributes:
        weight (float): Weight of the grader (must be between 0 and 1)
    """
    weight: float = Field(
        DEFAULT_WEIGHTED_GRADER_WEIGHT,
        description="Weight of the grader"
    )

    @field_validator('weight')
    @classmethod
    def validate_weight(cls, v: float) -> float:
        """Validate weight is between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError("Weight must be between 0 and 1")
        return v

