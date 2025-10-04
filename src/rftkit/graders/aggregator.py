"""AggregatorGrader for combining multiple grader scores using custom formulas."""

from typing import cast
from pydantic import Field
from ..base import MultiGrader
from .formatting import FormattingGrader


class AggregatorGrader(MultiGrader):
    """
    MultiGrader that aggregates scores using a weighted formula with indicator masking.
    
    The AggregatorGrader implements the cluster-based rubric aggregation formula:
    
    Final Score = Format_Score × Format_Weight + 
                  Σ(Indicator[i] × Rubric_Score[i] × Rubric_Weight[i])
    
    Key features:
    - FormattingGrader contributes directly with its weight
    - Each RubricGrader is multiplied by its corresponding IndicatorGrader score
    - IndicatorGrader acts as a 0/1 mask to exclude irrelevant rubrics
    - Supports cluster-based evaluation where only relevant rubrics contribute
    
    The rubric_to_indicator_map defines which IndicatorGrader corresponds to
    which RubricGrader, enabling the multiplicative masking.
    
    Attributes:
        rubric_to_indicator_map (dict[str, str]): Maps rubric grader names to indicator names
        formatting_grader_name (str): Name of the FormattingGrader in the graders list
        
    Examples:
        >>> from rftkit.graders import (
        ...     AggregatorGrader, FormattingGrader, RubricGrader, IndicatorGrader
        ... )
        >>> 
        >>> # Create individual graders
        >>> format_grader = FormattingGrader(name="format", weight=0.1)
        >>> rubric = RubricGrader(name="rubric_item_1", rubric={...}, weight=1.0)
        >>> indicator = IndicatorGrader(name="indicator_1", rubric_name="item_1")
        >>> 
        >>> # Aggregate them
        >>> aggregator = AggregatorGrader(
        ...     name="final_score",
        ...     graders=[format_grader, rubric, indicator],
        ...     rubric_to_indicator_map={"rubric_item_1": "indicator_1"},
        ...     formatting_grader_name="format"
        ... )
        >>> 
        >>> # Get the config with the formula
        >>> config = aggregator.config
        >>> print(config["calculate_output"])
        >>> # "(format * 0.1) + (indicator_1 * 1.0 * rubric_item_1)"
    """
    rubric_to_indicator_map: dict[str, str] = Field(
        ...,
        description="Map of rubric grader names to their corresponding indicator grader names"
    )
    formatting_grader_name: str = Field(
        ...,
        description="Name of the FormattingGrader in the graders list"
    )

    def _calculate_output(self) -> str:
        """
        Generate the formula for combining grader scores.
        
        The formula has two parts:
        1. FormattingGrader contribution: format_name * format_weight
        2. RubricGrader contributions: indicator_name * rubric_weight * rubric_name
        
        Returns:
            str: Formula string for score calculation
            
        Example output:
            "(format * 0.2) + (indicator_1 * 1.0 * rubric_1 + indicator_2 * 1.0 * rubric_2)"
        """
        # Get the FormattingGrader and calculate its contribution
        formatting_grader: FormattingGrader = cast(
            FormattingGrader,
            self.graders_dict[self.formatting_grader_name]
        )
        formatting_grade = f"{formatting_grader.name} * {formatting_grader.weight}"

        # Calculate RubricGrader contributions with indicator masking
        rubric_grade_terms = []
        for rubric_name, indicator_name in self.rubric_to_indicator_map.items():
            rubric_grader = self.graders_dict[rubric_name]
            indicator_grader = self.graders_dict[indicator_name]
            
            # Formula: indicator * weight * rubric
            # When indicator = 0 (irrelevant), entire term becomes 0
            # When indicator = 1 (relevant), rubric score is weighted normally
            term = f"{indicator_grader.name} * {rubric_grader.weight} * {rubric_grader.name}"
            rubric_grade_terms.append(term)

        # Combine all terms
        rubric_grade_summation = " + ".join(rubric_grade_terms)
        
        # Final formula: formatting + all rubric terms
        final_formula = f"({formatting_grade}) + ({rubric_grade_summation})"
        return final_formula

