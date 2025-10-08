"""Rubric grader prompt templates."""

from string import Template


RUBRIC_GRADER_PROMPT_TEMPLATE = Template(
    """
You are an expert grader. Evaluate the given output strictly against the rubric below and assign a score from 0.0 to 1.0.

Rubric Starts Here.

$rubric_content

Rubric Ends Here.

Scoring instructions:
- Score range: 0.0 (does not meet the rubric at all) to 1.0 (fully meets the rubric).
- Decimals are allowed (e.g., 0.73). Use the full scale when appropriate.
- Base your judgment only on the rubric and the provided output.

Output format:
- Respond with ONLY the numeric score (a single float between 0.0 and 1.0). Do not include any other text.
"""
)

