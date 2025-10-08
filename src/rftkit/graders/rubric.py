"""RubricGrader for LLM-based evaluation against structured criteria."""

from pydantic import Field
from ..base import ScoreModelGrader, WeightedGrader
from ..types import RubricItem, Message
from ..prompts.rubric import RUBRIC_GRADER_PROMPT_TEMPLATE


class RubricGrader(ScoreModelGrader, WeightedGrader):
    """
    Score model grader for evaluating outputs against a structured rubric.
    
    The RubricGrader uses OpenAI's scoring model to evaluate model outputs
    based on defined rubric criteria. Each rubric item represents a specific
    quality dimension (e.g., "Accuracy", "Completeness", "Clarity") with
    detailed scoring guidelines.
    
    The grader automatically constructs a prompt that includes:
    - System message with the rubric content
    - User message with reference answer and model output
    - OpenAI templating for dynamic content injection
    
    Rubric items should include:
    - id: Unique identifier for the rubric
    - content: Detailed description of the evaluation criteria
    
    The model returns a score from 0.0 to 1.0, which is then weighted and
    combined with other graders in the MultiGrader.
    
    Attributes:
        rubric (RubricItem): The rubric item to grade against
        
    Examples:
        >>> from rftkit.graders import RubricGrader
        >>> from rftkit.types import RubricItem
        >>> 
        >>> rubric = RubricItem(
        ...     id=1,
        ...     content="Accuracy: How correct and precise the output is..."
        ... )
        >>> grader = RubricGrader(
        ...     name="rubric_accuracy",
        ...     rubric=rubric,
        ...     weight=1.0
        ... )
        >>> config = grader.config
    """
    rubric: RubricItem = Field(..., description="Rubric item to grade against")

    def __init__(self, name: str, **kwargs):
        """
        Initialize the RubricGrader and create the input messages.
        
        Args:
            name: Unique identifier for this grader
            **kwargs: Additional arguments including rubric
        """
        super().__init__(name, **kwargs)
        self.create_input()

    def create_input(self) -> None:
        """
        Create RubricGrader input messages based on the rubric content.
        
        Constructs two messages:
        1. System message: Contains the rubric content and scoring instructions
        2. User message: Template that references the reference answer and model output
        """
        system_message: Message = {
            "role": "system",
            "content": RUBRIC_GRADER_PROMPT_TEMPLATE.substitute(
                rubric_content=self.rubric["content"]
            )
        }
        
        # Use OpenAI's templating to reference the sample and item
        user_message: Message = {
            "role": "user",
            "content": "Reference: {{ item.reference_answer }}. Model answer: {{ sample.output_text }}"
        }
        
        self.input.clear()  # Clear any default input
        self.input.append(system_message)
        self.input.append(user_message)

