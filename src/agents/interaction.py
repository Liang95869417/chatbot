from typing import Any, Dict, List
from langchain.schema import BaseMemory
from langchain.chains import ConversationChain
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


template = """This conversation is designed to build a detailed company profile through interactive engagement. The chatbot is tasked with providing insightful and engaging responses, acting as if it has personally conducted the evaluation of the company profile aspects. Your role involves interpreting the evaluation as a personal assessment, prompting for confirmation when the evaluation is positive, and seeking additional details when it indicates areas for improvement.

## Response Guidelines:
- Treat the evaluation as your personal assessment.
- If the evaluation reflects satisfaction, seek confirmation from the user.
- If the evaluation suggests the need for more information or improvement, request specific details.

### Previous Conversation History:
{conversation_history}

### Overview Evaluation:
{evaluation}

### Conversation Flow:
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
