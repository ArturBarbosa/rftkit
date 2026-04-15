# RFTKit - Reinforcement Fine-Tuning Toolkit

A comprehensive Python toolkit for [OpenAI's Reinforcement Fine-Tuning (RFT)](https://platform.openai.com/docs/guides/reinforcement-fine-tuning), featuring Pydantic-based grader creation, a Graders API SDK, and dataset utilities.

## Features

- **Pydantic-Based Graders**: Type-safe, validated grader definitions
- **Multiple Grader Types**: Python, Score Model, and Multi graders
- **Flexible Composition**: Combine graders with custom weighted formulas
- **OpenAI RFT Ready**: Export configs directly for OpenAI's RFT API

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
    RubricItem,
    export_grader_config,
)

# 1. Create a formatting grader (validates JSON structure)
format_grader = FormattingGrader(
    name="format_validator",
    weight=0.2
)

# 2. Create a rubric grader (LLM-based evaluation)
rubric = RubricItem(
    id=1,
    content="Accuracy: How correct and precise the output is. 0.0 = incorrect, 1.0 = perfect"
)
rubric_grader = RubricGrader(
    name="rubric_accuracy",
    rubric=rubric,
    weight=1.0
)

# 3. Export config for OpenAI RFT API
export_grader_config(rubric_grader, "grader_config.json")
```

## Grader Types

### FormattingGrader

A `PythonGrader` that validates JSON structure and required fields:

```python
format_grader = FormattingGrader(
    name="json_validator",
    weight=0.2
)
```

### RubricGrader

A `ScoreModelGrader` that uses an LLM to evaluate outputs against specific criteria:

```python
rubric = RubricItem(
    id=1,
    content="Detailed rubric description with scoring guidelines..."
)
rubric_grader = RubricGrader(
    name="rubric_name",
    rubric=rubric,
    weight=1.0,
    model="gpt-4o-2024-08-06"
)
```

### Base Classes

RFTKit provides base classes you can extend to build custom graders:

- **`PythonGrader`**: Execute custom Python code for evaluation
- **`ScoreModelGrader`**: Use an LLM to assign scores (0-1)
- **`MultiGrader`**: Combine multiple graders with a custom formula
- **`WeightedGrader`**: Mixin that adds a `weight` field (0-1)

## OpenAI RFT Integration

Use the exported config directly with OpenAI's API:

```python
import openai

client = openai.OpenAI()

# Create RFT job with your grader
job = client.fine_tuning.jobs.create(
    training_file="file-abc123",
    model="gpt-4o-2024-08-06",
    method={
        "type": "reinforcement",
        "reinforcement": {
            "grader": rubric_grader.config
        }
    }
)
```

## Examples

See the `examples/` directory for Jupyter notebooks demonstrating:

- Basic grader usage
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
