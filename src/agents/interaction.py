from typing import Any, Dict, List
from langchain.schema import BaseMemory
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from src.llm_providers.chat_model_provider import llm, llm4
from langchain.prompts import PromptTemplate
from pydantic import BaseModel


class ConversationMemoryData(BaseModel):
    """Data model for conversation memory using Pydantic for validation."""

    conversation_history: List[Dict[str, Any]] = []
    evaluation: str = ""


class CustomConversationMemory(BaseMemory):
    """Custom memory class for storing conversation history, overview, and overview evaluation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Directly set the attribute to bypass Pydantic's __setattr__
        object.__setattr__(self, "data", ConversationMemoryData())

    def clear(self):
        # Reset the data to a new instance
        object.__setattr__(self, "data", ConversationMemoryData())

    @property
    def memory_variables(self) -> List[str]:
        """Defines the variables provided to the prompt."""
        return [
            "conversation_history",
            "evaluation",
        ]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Loads the memory variables to be used in the prompt."""
        memory_context = {
            "conversation_history": "\n".join(
                [str(msg) for msg in self.data.conversation_history]
            ),
            "evaluation": self.data.evaluation,
        }
        return memory_context

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Saves context from the conversation to memory."""
        self.data.conversation_history.append(
            {"input": inputs.get("input"), "output": outputs.get("response")}
        )

    def set_evaluation(self, evaluation: dict):
        """Updates the evaluation of the general overview in memory."""
        self.data.evaluation = evaluation


template = """
This conversation is an interactive session aimed at constructing a nuanced company profile. Acting as a Company Profile Analyst, I will share evaluations as if I have personally examined various aspects of the company. Your task is to engage with these evaluations as if they were your own insights, asking for confirmation to affirm positive assessments and delving deeper where improvements or additional details are necessary.

# Response Guidelines:
Embrace the Evaluation: Treat evaluations as your own insights. Starting by saying that I have evaluated the company profile or Based on evaluation or similar...
Seek Confirmation: If an evaluation indicates satisfaction, prompt the user to confirm this assessment.
Request Details: Where the evaluation suggests a need for more information or highlights areas for improvement, inquire about specific details to enhance understanding.

# Previous Conversation History:
{conversation_history}

# Your Evaluation:
{evaluation}

# Conversation Flow:
Human: {input}
AI: 
"""

prompt = PromptTemplate(
    input_variables=[
        "conversation_history",
        "evaluation",
        "input",
    ],
    template=template,
)

custom_memory = CustomConversationMemory()

interaction_chain = ConversationChain(
    llm=llm, prompt=prompt, verbose=True, memory=custom_memory
)
