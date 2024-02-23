from pydantic.v1 import BaseModel, Field


class EvaluationOutput(BaseModel):
    is_satisfied: bool = Field(
        description="Whether the current aspect of company profile is satisfied or not based on criteria."
    )
    message: str = Field(
        description="Here is details about evaluation result.",
    )
