"""Configuration constants for RFT graders."""

# ====== Default weights for graders ===========
DEFAULT_WEIGHTED_GRADER_WEIGHT = 1.0

# ====== Python Grader ===========
# Default image tag for graders
DEFAULT_IMAGE_TAG = "2025-05-08"

# ====== Score Model Grader ===========
# Default model for score graders
DEFAULT_SCORE_MODEL = "gpt-4o-2024-08-06"

# Default scoring range (Likert scale: 1-5)
DEFAULT_SCORE_RANGE = [1, 5]

# Default pass threshold (middle of 1-5 scale)
DEFAULT_PASS_THRESHOLD = 3

# Default input prompt for score model graders
DEFAULT_SCORE_INPUT = []

# Default sampling parameters for score model graders
DEFAULT_SAMPLING_PARAMS = {
    "seed": 42,
    "max_completion_tokens": 32768, 
    "reasoning_effort": "medium"
}

