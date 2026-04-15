"""Utility functions for RFTKit grader management."""

from typing import Dict, Any
import json
from pathlib import Path


def export_grader_config(grader, output_path: str) -> None:
    """
    Export a grader configuration to a JSON file.
    
    Args:
        grader: Any grader instance with a config property
        output_path: Path to save the configuration file
        
    Example:
        >>> from rftkit import RubricGrader
        >>> grader = RubricGrader(...)
        >>> export_grader_config(grader, "grader_config.json")
    """
    config = grader.config
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)


def load_grader_config(input_path: str) -> Dict[str, Any]:
    """
    Load a grader configuration from a JSON file.
    
    Args:
        input_path: Path to the configuration file
        
    Returns:
        Dictionary containing the grader configuration
        
    Example:
        >>> config = load_grader_config("grader_config.json")
        >>> # Use with OpenAI API
    """
    with open(input_path, 'r') as f:
        return json.load(f)


def validate_grader_config(config: Dict[str, Any]) -> bool:
    """
    Validate that a grader configuration has required fields.
    
    Args:
        config: Grader configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["name", "type"]
    
    for field in required_fields:
        if field not in config:
            return False
    
    # Type-specific validation
    grader_type = config["type"]
    
    if grader_type == "python":
        if "source" not in config:
            return False
    elif grader_type == "string_check":
        required = ["input", "reference", "operation"]
        if not all(field in config for field in required):
            return False
    elif grader_type == "text_similarity":
        required = ["input", "reference", "evaluation_metric", "pass_threshold"]
        if not all(field in config for field in required):
            return False
    elif grader_type == "score_model":
        required = ["model", "input", "range", "pass_threshold"]
        if not all(field in config for field in required):
            return False
    elif grader_type == "multi":
        if "graders" not in config or "calculate_output" not in config:
            return False
    
    return True


def summarize_grader_config(config: Dict[str, Any]) -> str:
    """
    Create a human-readable summary of a grader configuration.
    
    Args:
        config: Grader configuration dictionary
        
    Returns:
        String summary of the grader
    """
    lines = []
    lines.append(f"Grader: {config['name']}")
    lines.append(f"Type: {config['type']}")
    
    if config['type'] == 'multi':
        num_graders = len(config.get('graders', {}))
        lines.append(f"Sub-graders: {num_graders}")
        lines.append(f"Formula: {config.get('calculate_output', 'N/A')}")
    elif config['type'] == 'score_model':
        lines.append(f"Model: {config.get('model', 'N/A')}")
        lines.append(f"Range: {config.get('range', 'N/A')}")
    elif config['type'] == 'python':
        source_lines = len(config.get('source', '').split('\n'))
        lines.append(f"Source code: {source_lines} lines")
    
    return '\n'.join(lines)

