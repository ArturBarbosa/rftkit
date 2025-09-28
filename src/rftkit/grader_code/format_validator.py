"""Format validation grader for structured activity output."""

from typing import Any, List, Dict


def grade(sample: dict[str, Any], item: dict[str, Any]) -> float:
    """
    Validates the format of an activity object based on expected structure.
    Returns 1.0 if valid, 0.0 if invalid.
    
    This validator checks for:
    - Valid JSON structure in content field
    - Presence of required fields (interactions, answers)
    - Valid interaction types and structures
    - Valid answer structures
    - Proper matching between interactions and answers
    
    Args:
        sample: Dict containing the model's output
        item: Dict containing the reference/input data
        
    Returns:
        float: 1.0 if format is valid, 0.0 otherwise
    """
    try:
        # Check if content exists
        if "content" not in sample:
            return 0.0
        
        content = sample["content"]
        
        # Validate required content fields
        if not isinstance(content, dict):
            return 0.0
        
        # Check interactions array exists and is not empty
        if "interactions" not in content or not isinstance(content.get("interactions"), list):
            return 0.0
        
        interactions = content["interactions"]
        if len(interactions) == 0:
            return 0.0
        
        # Check answers array exists (can be empty)
        if "answers" not in content or not isinstance(content.get("answers"), list):
            return 0.0
        
        answers = content["answers"]
        
        # Validate each interaction
        for idx, interaction in enumerate(interactions):
            if not validate_interaction(interaction, idx):
                return 0.0
        
        # Validate each answer
        for answer in answers:
            if not validate_answer(answer):
                return 0.0
        
        # Validate that interactions needing replies have answers
        if not validate_interaction_answer_matching(interactions, answers):
            return 0.0
        
        return 1.0
    
    except Exception:
        return 0.0


def validate_interaction(interaction: Dict[str, Any], idx: int) -> bool:
    """
    Validates a single interaction based on its kind.
    
    Args:
        interaction: The interaction dict to validate
        idx: Index of the interaction in the list
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(interaction, dict):
        return False
    
    # Required base fields
    required_fields = ["kind", "from"]
    for field in required_fields:
        if field not in interaction:
            return False
    
    # Validate 'from' field
    if interaction["from"] not in ["user", "bot", "system"]:
        return False
    
    # Validate 'kind' field and kind-specific validation
    kind = interaction["kind"]
    valid_kinds = [
        "text", "audio", "audio:text", "image", "select", "drawer",
        "video", "button", "carousel", "alert", "tag", "delay",
        "redirect", "sticker", "document", "contact", "answer",
        "audioBuffer", "audioBuffer:text", "audioChunk", "textDelta"
    ]
    
    if kind not in valid_kinds:
        return False
    
    # Kind-specific validation
    if kind == "text":
        if "text" not in interaction or not isinstance(interaction["text"], (str, type(None))):
            return False
    
    elif kind == "image":
        if "imageURL" not in interaction or not isinstance(interaction["imageURL"], (str, type(None))):
            return False
    
    elif kind == "drawer":
        if "from" in interaction and interaction["from"] not in ["system", "bot"]:
            return False
        if "drawerTitle" not in interaction or "title" not in interaction or "body" not in interaction:
            return False
    
    elif kind == "select":
        if "options" not in interaction or not isinstance(interaction.get("options"), (list, type(None))):
            return False
        if interaction.get("options") and len(interaction["options"]) > 0:
            for option in interaction["options"]:
                if not isinstance(option, dict) or "text" not in option:
                    return False
    
    elif kind in ["audio", "audio:text"]:
        if "audioURL" not in interaction:
            return False
        if kind == "audio:text" and "text" not in interaction:
            return False
    
    elif kind == "video":
        if "videoURL" not in interaction:
            return False
    
    # Validate needsReply structure
    if "needsReply" in interaction:
        if not isinstance(interaction["needsReply"], bool):
            return False
        
        if interaction["needsReply"] is True:
            # When needsReply is true, replyTypes should exist
            if "replyTypes" not in interaction or not isinstance(interaction["replyTypes"], list):
                return False
            
            # Validate replyTypes values
            valid_reply_types = ["audio", "text"]
            for reply_type in interaction["replyTypes"]:
                if reply_type not in valid_reply_types:
                    return False
    
    return True


def validate_answer(answer: Dict[str, Any]) -> bool:
    """
    Validates a single answer object.
    
    Args:
        answer: The answer dict to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(answer, dict):
        return False
    
    # Must have interactionId
    if "interactionId" not in answer:
        return False
    
    # Must have exactMatch field
    if "exactMatch" not in answer:
        return False
    
    exact_match = answer["exactMatch"]
    
    if exact_match is True:
        # ExactAnswer: must have 'answer' field
        if "answer" not in answer:
            return False
    elif exact_match is False:
        # ApproximateAnswer: must have 'answers' array
        if "answers" not in answer or not isinstance(answer["answers"], list):
            return False
    else:
        # exactMatch must be boolean
        return False
    
    return True


def validate_interaction_answer_matching(interactions: List[Dict], answers: List[Dict]) -> bool:
    """
    Validates that interactions needing replies have corresponding answers.
    
    Args:
        interactions: List of interaction dicts
        answers: List of answer dicts
        
    Returns:
        bool: True if matching is valid, False otherwise
    """
    # Get all interactions that need replies and have an _id
    interactions_needing_reply = [
        interaction for interaction in interactions
        if interaction.get("needsReply") is True and "_id" in interaction
    ]
    
    # Check each interaction that needs a reply has a corresponding answer
    for interaction in interactions_needing_reply:
        interaction_id = str(interaction["_id"])
        has_answer = any(
            answer.get("interactionId") == interaction_id 
            for answer in answers
        )
        if not has_answer:
            return False
    
    # Validate answers reference valid interactions
    for answer in answers:
        interaction_id = answer.get("interactionId")
        if interaction_id is None:
            continue
        
        # Try to find by _id first
        found_by_id = any(
            str(interaction.get("_id")) == str(interaction_id)
            for interaction in interactions
        )
        
        if not found_by_id:
            # Try as index if not found by _id
            try:
                idx = int(interaction_id)
                if idx < 0 or idx >= len(interactions):
                    return False
            except (ValueError, TypeError):
                # If it's not a valid index and wasn't found by _id, it's invalid
                return False
    
    return True

