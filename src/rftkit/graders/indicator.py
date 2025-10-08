"""IndicatorGrader for cluster-based rubric selection."""

from pydantic import Field
from ..base import PythonGrader


class IndicatorGrader(PythonGrader):
    """
    Python grader for determining rubric relevance based on data type/cluster.
    
    The IndicatorGrader implements the cluster-based rubric system by returning
    1.0 if a rubric applies to the current data type (cluster) and 0.0 if it
    doesn't. This allows the MultiGrader to filter out irrelevant rubrics by
    multiplying their scores by 0.
    
    Each data type/cluster has its own specific set of rubrics. For example,
    "cluster_a" might have 8 rubrics focused on accuracy and completeness, while
    "cluster_b" has different rubrics focused on performance and scalability.
    
    The rubric name is injected into the source code via template replacement,
    allowing multiple IndicatorGrader instances to share the same base code
    while checking different rubric names.
    
    Attributes:
        rubric_name (str): Name of the rubric to check for relevance
        module_path (str): Path to the indicator validation module
    
    Examples:
        >>> from rftkit.graders import IndicatorGrader
        >>> indicator = IndicatorGrader(
        ...     name="indicator_accuracy",
        ...     rubric_name="accuracy"
        ... )
        >>> config = indicator.config
        >>> # The source code will contain the specific rubric name
    """
    rubric_name: str = Field(..., description="Name of the rubric to check")
    module_path: str = Field(
        default="rftkit.grader_code.indicator_validator",
        description="Python source code module path"
    )

    def process_code(self, code_str: str) -> str:
        """
        Replace the rubric name placeholder with the actual rubric name.
        
        This allows the same indicator validation code to be used for different
        rubrics by simply substituting the rubric name.
        
        Args:
            code_str: The source code with placeholder
            
        Returns:
            The source code with the placeholder replaced by the actual rubric name
        """
        return code_str.replace("<rubric_name>", self.rubric_name)

