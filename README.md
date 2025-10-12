# RFTKit - Reinforcement Fine-Tuning Toolkit

A comprehensive Python toolkit for OpenAI's Reinforcement Fine-Tuning (RFT), featuring Pydantic-based grader creation, cluster-based rubric evaluation, and seamless OpenAI API integration.

## Features

- 🎯 **Cluster-Based Rubric System**: Automatically filter rubrics based on activity type
- 🔧 **Pydantic-Based Graders**: Type-safe, validated grader definitions
- 📊 **Multiple Grader Types**: Python, Score Model, and Multi graders
- 🎨 **Flexible Aggregation**: Combine graders with custom weighted formulas
- 🚀 **OpenAI RFT Ready**: Export configs directly for OpenAI's RFT API

## Installation

```bash
pip install rftkit
```

Or install from source:

```bash
git clone https://github.com/yourusername/rftkit.git
cd rftkit
pip install -e .
```

## Quick Start

```python
from rftkit import (
    FormattingGrader,
    RubricGrader,
    IndicatorGrader,
    AggregatorGrader,
    RubricItem
)

# 1. Create a formatting grader
format_grader = FormattingGrader(
    name="format_validator",
    weight=0.2
)

# 2. Create a rubric grader
rubric = RubricItem(
    id=1,
    content="Accuracy: How correct and precise the output is. Evaluate on a 1-5 Likert scale."
)
rubric_grader = RubricGrader(
    name="rubric_accuracy",
    rubric=rubric,
    weight=1.0
)

# 3. Create an indicator grader (cluster-based filtering)
indicator = IndicatorGrader(
    name="indicator_accuracy",
    rubric_name="accuracy"
)

# 4. Combine with aggregator
aggregator = AggregatorGrader(
    name="final_score",
    graders=[format_grader, rubric_grader, indicator],
    rubric_to_indicator_map={"rubric_accuracy": "indicator_accuracy"},
    formatting_grader_name="format_validator"
)

# 5. Export for OpenAI RFT API
config = aggregator.config
```

## Architecture

### Cluster-Based Rubric System

RFTKit implements a cluster-based evaluation system where each data type/cluster has its own specific set of rubrics:

```
┌─────────────────────────────────────────────────────────┐
│                    Input Data                            │
│                  (e.g., Model output)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Cluster Type Detection                  │
│              (Extract type from content)                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Indicator Grader                       │
│         (Determines which rubrics apply)                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Rubric 1 │  │ Rubric 2 │  │ Rubric N │
│ (Active) │  │ (Active) │  │(Inactive)│
│ Score:4.2│  │ Score:4.5│  │ Score:0  │
└──────────┘  └──────────┘  └──────────┘
        │            │            │
        └────────────┼────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Aggregator Grader                      │
│                                                          │
│  Final = Format_Score +                                 │
│          Σ(Indicator[i] × Weight[i] × Rubric_Score[i]) │
└─────────────────────────────────────────────────────────┘
```

### Mathematical Model

The final score is calculated using the formula:

```
S = s_F · w_F + Σ(s_c,i · w_r,i · s_r,i)
```

Where:
- `S`: Final score
- `s_F`: FormattingGrader score
- `w_F`: FormattingGrader weight
- `s_r,i`: Rubric grader i's score
- `w_r,i`: Rubric grader i's weight
- `s_c,i`: Indicator grader i's score (0 or 1)

The indicator score acts as a binary mask, zeroing out irrelevant rubrics for each activity type.

## Grader Types

### FormattingGrader

Validates JSON structure and required fields using Python code:

```python
format_grader = FormattingGrader(
    name="json_validator",
    weight=0.2
)
```

### RubricGrader

Uses LLMs to evaluate outputs against specific criteria using a 1-5 Likert scale:

```python
rubric = RubricItem(
    id=1,
    content="Detailed rubric description with scoring guidelines..."
)
rubric_grader = RubricGrader(
    name="rubric_name",
    rubric=rubric,
    weight=1.0,
    model="gpt-4o-2024-08-06",
    range=[1, 5],  # Default Likert scale
    pass_threshold=3  # Default threshold
)
```

### IndicatorGrader

Determines rubric relevance based on activity type:

```python
indicator = IndicatorGrader(
    name="indicator_name",
    rubric_name="rubric_identifier"
)
```

### AggregatorGrader

Combines multiple graders with a weighted formula:

```python
aggregator = AggregatorGrader(
    name="final_score",
    graders=[format_grader, rubric_grader, indicator],
    rubric_to_indicator_map={"rubric": "indicator"},
    formatting_grader_name="format"
)
```

## Cluster Configuration

Define which rubrics apply to which data types/clusters by modifying the cluster mapping in `indicator_validator.py`:

```python
cluster_to_rubric_map = {
    "cluster_a": [
        "accuracy",
        "completeness",
        "clarity",
        # ... more rubrics
    ],
    "cluster_b": [
        "efficiency",
        "scalability",
        "performance",
        # ... different rubrics
    ],
}
```

## OpenAI RFT Integration

Use the exported config directly with OpenAI's API:

```python
import openai

client = openai.OpenAI()

# Create RFT job with your grader
job = client.fine_tuning.jobs.create(
    training_file="file-abc123",
    model="gpt-4o-2024-08-06",
    hyperparameters={
        "n_epochs": 3
    },
    grader=aggregator.config  # Use your grader config
)
```

## Examples

See the `examples/` directory for Jupyter notebooks demonstrating:

- Basic grader usage
- Cluster-based rubric configuration
- Multi-grader aggregation
- OpenAI RFT integration

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/rftkit.git
cd rftkit

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [OpenAI RFT Documentation](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- [OpenAI Graders Documentation](https://platform.openai.com/docs/guides/graders)

## Citation

If you use RFTKit in your research, please cite:

```bibtex
@software{rftkit2024,
  title={RFTKit: Reinforcement Fine-Tuning Toolkit},
  author={Barbosa, Artur},
  year={2024},
  url={https://github.com/yourusername/rftkit}
}
```
