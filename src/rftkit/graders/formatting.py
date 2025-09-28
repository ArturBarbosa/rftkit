"""FormattingGrader for validating JSON structure of model outputs."""

from pydantic import Field
from ..base import PythonGrader, WeightedGrader


class FormattingGrader(PythonGrader, WeightedGrader):
    """
    Python grader for validating the JSON structure of model outputs.
    
    This grader checks that the output conforms to the expected structure:
    - Valid JSON format
    - Required fields present (content, interactions, answers)
    - Valid interaction types and structures
    - Proper answer structures
    - Correct matching between interactions and answers
    
    The grader returns a binary score:
    - 1.0 if the output is correctly formatted
    - 0.0 if there are any formatting errors
    
    Examples:
        >>> from rftkit.graders import FormattingGrader
        >>> grader = FormattingGrader(name="json_validator")
        >>> config = grader.config
        >>> print(config["type"])  # "python"
    """
    module_path: str = Field(
        default="rftkit.grader_code.format_validator",
        description="Python source code module path"
    )

