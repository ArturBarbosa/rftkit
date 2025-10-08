"""Format validation grader for structured output."""

from typing import Any
import json


def grade(sample: dict[str, Any], item: dict[str, Any]) -> float:
    """
    Validates the format of a data object based on expected structure.
    Returns 1.0 if valid, 0.0 if invalid.
    
    This is a customizable validator - modify the validation logic for your domain.
    
    Example validation checks:
    - Valid JSON structure
    - Presence of required fields
    - Valid data types for each field
    - Proper relationships between fields
    - Schema compliance
    
    Args:
        sample: Dict containing the model's output
        item: Dict containing the reference/input data
        
    Returns:
        float: 1.0 if format is valid, 0.0 otherwise
    """
    try:
        # Example validation: Check basic structure
        # Customize this for your specific data format
        
        # Check if output_text exists (common in RFT)
        output = sample.get("output_text", sample)
        
        # Try to parse as JSON if it's a string
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                return 0.0
        
        # Example: Validate that output is a dictionary
        if not isinstance(output, dict):
            return 0.0
        
        # Example: Check for required keys
        # Customize these required fields for your domain
        required_fields = ["data", "metadata"]
        for field in required_fields:
            if field not in output:
                # If field is missing, you might want to return 0.0
                # or be more lenient depending on your use case
                pass
        
        # Example: Validate data types if fields exist
        if "data" in output and not isinstance(output["data"], (list, dict)):
            return 0.0
        
        if "metadata" in output and not isinstance(output["metadata"], dict):
            return 0.0
        
        # All validations passed
        return 1.0
    
    except Exception:
        return 0.0
