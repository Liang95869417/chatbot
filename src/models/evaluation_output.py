from pydantic.v1 import BaseModel, Field
from typing import Optional

class EvaluationOutput(BaseModel):
    is_satisfied: bool = Field(
        description="Whether the current aspect of company profile is satisfied or not based on criteria."
    )
    evaluation: str = Field(
        description="Here is details about evaluation result.",
    )
    questions: Optional[str]= Field(
        description="Here is questions to ask.",
    )
