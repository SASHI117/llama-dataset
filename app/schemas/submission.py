from pydantic import BaseModel
from typing import List, Optional

class QAPair(BaseModel):
    question: str
    answer: str

class SubmissionRequest(BaseModel):
    crop: str
    behavior: str
    qa_pairs: List[QAPair]
