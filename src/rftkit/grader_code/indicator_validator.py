"""Indicator validator for cluster-based rubric selection."""

from typing import Any
import json


def grade(sample: dict[str, Any], item: dict[str, Any]) -> float:
    """
    Determines whether a rubric item is relevant for a specific activity type.
    Returns 1.0 if relevant (indicator = 1), 0.0 if irrelevant (indicator = 0).
    
    This implements the cluster-based rubric system where each activity format
    (cluster) has its own set of specific evaluation criteria. By returning 0
    for irrelevant rubrics, we ensure they don't contribute to the final score.

    Args:
        sample: Dict containing the model's output
        item: Dict containing the reference/input data

    Returns:
        float: 1.0 if the rubric is valid for this activity type, 0.0 otherwise
    """
    # Activity type to rubric mapping - defines which rubrics apply to which clusters
    activity_type_to_rubric_item_map = {
        "ChatConsolidateLexisGrammarTeacher": [
            "alignment_to_purpose",
            "feedback_and_modeling",
            "focus_on_noticing",
            "input_quality",
            "mcq_distractor_quality",
            "multimodality_use",
            "summary_and_final_consolidation",
            "variety_and_relevance_of_questions",
        ],
        "ChatIntroduceLexisTeacher": [
            "active_participation",
            "alignment_to_purpose",
            "complete_learning_cycle",
            "final_mcq_quality",
            "lexical_input_quality",
            "multimodality",
            "plausible_distractors",
            "tone_and_engagement",
        ],
        "ChatTestLexisGrammarChallenge": [
            "alignment_to_purpose",
            "feedback_and_scaffolding",
            "focus_on_form_and_use",
            "implicit_correction",
            "mcq_quality",
            "multimodality",
            "summary_and_closure",
            "variety_of_formats",
        ],
        "ChatTestListeningActivity": [
            "alignment_to_purpose",
            "engagement_and_tone",
            "feedback_and_reinforcement",
            "final_transcription",
            "input_authenticity",
            "mcq_quality",
            "scaffolding",
            "top_down_vs_bottom_up_balance",
        ],
        "ChatTestPronunciationChallenge": [
            "clarity_and_naturalness_of_input",
            "focus_on_phonetic_prosodic_target",
            "multimodal_integration",
            "noticing_without_metalanguage",
            "perception_mcq_quality",
            "practice_cycle",
            "scaffolding_and_progression",
            "summary_and_closure",
        ],
        "VideoConsolidateGrammarEnglishInAction": [
            "alignment_to_purpose",
            "closure",
            "communicative_authenticity",
            "focus_on_form_and_context",
            "implicit_feedback",
            "mcq_quality_complete_answers",
            "multimodality_use",
            "opening_and_contextualization",
        ],
        "VideoConsolidateLexisGrammarHelpers": [
            "alignment_to_purpose",
            "closure_and_feedback",
            "communicative_authenticity",
            "grammar_lexis_integration",
            "mcq_quality",
            "multimodality_use",
            "opening_and_contextualization",
            "scaffolding_and_progression",
        ],
        "VideoIntroduceGrammarClassroom": [
            "alignment_to_purpose",
            "mcq_quality",
            "multimodality_use",
            "noticing_and_implicit_contrast",
            "opening_and_contextualization",
            "progression_and_scaffolding",
            "summary_and_final_consolidation",
            "variety_and_quality_of_interactions",
        ],
        "VideoIntroduceLexisEnglishInAction": [
            "alignment_to_purpose",
            "communicative_focus_and_scaffolding",
            "level_appropriateness_cefr",
            "mcq_quality",
            "multimodality_use",
            "naturalness_of_introduction",
            "noticing_comprehension_fixation_cycle",
            "summary_and_final_consolidation",
        ],
    }

    # This placeholder will be replaced by IndicatorGrader.process_code()
    rubric_name = "<rubric_name>"

    try:
        activity_type = None

        # Try different ways to extract the activity type from the sample
        # Method 1: Check if there's an output_text field (common in RFT)
        if "output_text" in sample:
            try:
                output_data = json.loads(sample["output_text"])
                if isinstance(output_data, dict) and "format" in output_data:
                    activity_type = output_data["format"]
            except (json.JSONDecodeError, TypeError):
                pass

        # Method 2: Check if content field exists
        if not activity_type and "content" in sample:
            content = sample["content"]
            if isinstance(content, dict) and "format" in content:
                activity_type = content["format"]

        # Method 3: Direct format field in sample
        if not activity_type and "format" in sample:
            activity_type = sample["format"]

        # Method 4: Check the reference answer in item for activity type
        if not activity_type and item and "reference_answer" in item:
            try:
                ref_data = json.loads(item["reference_answer"]) if isinstance(
                    item["reference_answer"], str) else item["reference_answer"]
                if isinstance(ref_data, dict) and "format" in ref_data:
                    activity_type = ref_data["format"]
            except (json.JSONDecodeError, TypeError):
                pass

        # If we couldn't find the activity type, return 0
        if not activity_type:
            return 0.0

        # Check if the activity type is known
        if activity_type not in activity_type_to_rubric_item_map:
            # Unknown activity type - rubric is not applicable
            return 0.0

        # Get the list of valid rubrics for this activity type (cluster)
        valid_rubrics = activity_type_to_rubric_item_map[activity_type]

        # Check if the rubric is valid for this activity type
        if rubric_name in valid_rubrics:
            return 1.0  # Indicator = 1: Rubric applies to this cluster
        else:
            return 0.0  # Indicator = 0: Rubric doesn't apply to this cluster

    except Exception:
        # In case of any unexpected error, return 0
        return 0.0

