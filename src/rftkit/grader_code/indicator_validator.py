"""Indicator validator for cluster-based rubric selection."""

from typing import Any
import json


def grade(sample: dict[str, Any], item: dict[str, Any]) -> float:
    """
    Determines whether a rubric item is relevant for a specific data type/cluster.
    Returns 1.0 if relevant (indicator = 1), 0.0 if irrelevant (indicator = 0).
    
    This implements the cluster-based rubric system where each data type
    (cluster) has its own set of specific evaluation criteria. By returning 0
    for irrelevant rubrics, we ensure they don't contribute to the final score.

    Args:
        sample: Dict containing the model's output
        item: Dict containing the reference/input data

    Returns:
        float: 1.0 if the rubric is valid for this cluster type, 0.0 otherwise
    """
    # Cluster type to rubric mapping - defines which rubrics apply to which clusters
    # This is a customizable mapping that you should modify for your domain
    cluster_to_rubric_map = {
        "cluster_a": [
            "accuracy",
            "completeness",
            "clarity",
            "consistency",
            "relevance",
            "structure",
            "depth",
            "coherence",
        ],
        "cluster_b": [
            "accuracy",
            "efficiency",
            "scalability",
            "reliability",
            "performance",
            "maintainability",
            "documentation",
            "usability",
        ],
        "cluster_c": [
            "correctness",
            "precision",
            "recall",
            "coverage",
            "validity",
            "robustness",
            "generalization",
            "interpretability",
        ],
    }

    # This placeholder will be replaced by IndicatorGrader.process_code()
    rubric_name = "<rubric_name>"

    try:
        cluster_type = None

        # Try different ways to extract the cluster type from the sample
        # Method 1: Check if there's an output_text field (common in RFT)
        if "output_text" in sample:
            try:
                output_data = json.loads(sample["output_text"])
                if isinstance(output_data, dict) and "type" in output_data:
                    cluster_type = output_data["type"]
                elif isinstance(output_data, dict) and "cluster" in output_data:
                    cluster_type = output_data["cluster"]
            except (json.JSONDecodeError, TypeError):
                pass

        # Method 2: Check if there's a direct type or cluster field
        if not cluster_type and "type" in sample:
            cluster_type = sample["type"]
        
        if not cluster_type and "cluster" in sample:
            cluster_type = sample["cluster"]

        # Method 3: Check the reference answer in item
        if not cluster_type and item and "reference_answer" in item:
            try:
                ref_data = json.loads(item["reference_answer"]) if isinstance(
                    item["reference_answer"], str) else item["reference_answer"]
                if isinstance(ref_data, dict):
                    if "type" in ref_data:
                        cluster_type = ref_data["type"]
                    elif "cluster" in ref_data:
                        cluster_type = ref_data["cluster"]
            except (json.JSONDecodeError, TypeError):
                pass

        # If we couldn't find the cluster type, return 0
        if not cluster_type:
            return 0.0

        # Check if the cluster type is known
        if cluster_type not in cluster_to_rubric_map:
            # Unknown cluster type - rubric is not applicable
            return 0.0

        # Get the list of valid rubrics for this cluster type
        valid_rubrics = cluster_to_rubric_map[cluster_type]

        # Check if the rubric is valid for this cluster type
        if rubric_name in valid_rubrics:
            return 1.0  # Indicator = 1: Rubric applies to this cluster
        else:
            return 0.0  # Indicator = 0: Rubric doesn't apply to this cluster

    except Exception:
        # In case of any unexpected error, return 0
        return 0.0

