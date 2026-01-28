VALID_BEHAVIORS = {
    "theoretical",
    "practical",
    "calculation",
    "diagnostic",
    "preventive",
    "safety",
}

def validate_behavior(behavior: str):
    if behavior not in VALID_BEHAVIORS:
        raise ValueError("Invalid behavior type")

def validate_crop(crop: str):
    if not crop or not crop.strip():
        raise ValueError("Invalid crop name")

def validate_qa(question: str, answer: str):
    if not question.strip() or not answer.strip():
        raise ValueError("Question and Answer cannot be empty")
