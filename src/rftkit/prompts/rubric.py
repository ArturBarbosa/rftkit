"""Rubric grader prompt templates."""

from string import Template


RUBRIC_GRADER_PROMPT_TEMPLATE = Template(
    """
You are an expert grader. Evaluate the given output strictly against the rubric below and assign a score from 1 to 5.

Rubric Starts Here.

$rubric_content

Rubric Ends Here.

Scoring instructions (Likert scale):
- 1: Strongly disagrees with rubric / Does not meet criteria at all
- 2: Disagrees with rubric / Minimally meets criteria
- 3: Neutral / Partially meets criteria
- 4: Agrees with rubric / Mostly meets criteria
- 5: Strongly agrees with rubric / Fully meets criteria
- Decimals are allowed (e.g., 3.5, 4.2). Use the full scale when appropriate.
- Base your judgment only on the rubric and the provided output.

Output format:
- Respond with ONLY the numeric score (a single number between 1 and 5). Do not include any other text.
"""
)

