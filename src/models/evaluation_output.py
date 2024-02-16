from pydantic import BaseModel, Field


class EvaluationOutput(BaseModel):
    is_satisfied: bool = Field(
        description="If the aspect of company profile is satisfied or not."
    )
    Message: str = Field(
        description="Here is evaluation details.",
    )
