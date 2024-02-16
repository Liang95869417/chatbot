from typing import Any, Dict, List
from langchain.schema import BaseMemory
from langchain.chains import ConversationChain
from src.llm_providers.chat_model_provider import llm
from langchain.prompts import PromptTemplate
from pydantic import BaseModel


class ConversationMemoryData(BaseModel):
    """Data model for conversation memory using Pydantic for validation."""

    conversation_history: List[Dict[str, Any]] = []
    aspect: str = ""
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
            "aspect",
            "evaluation",
        ]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Loads the memory variables to be used in the prompt."""
        memory_context = {
            "conversation_history": "\n".join(
                [str(msg) for msg in self.data.conversation_history]
            ),
            "aspect": self.data.aspect,
            "evaluation": self.data.evaluation,
        }
        return memory_context

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Saves context from the conversation to memory."""
        self.data.conversation_history.append(
            {"input": inputs.get("input"), "output": outputs.get("response")}
        )
        # Implement logic to update `aspect` and `evaluation` here
        self.data.aspect = inputs.get("aspect")
        self.data.evaluation = inputs.get("evaluation")

    def set_aspect(self, aspect: str):
        """Updates the general overview in memory."""
        self.data.aspect = aspect

    def set_evaluation(self, evaluation: dict):
        """Updates the evaluation of the general overview in memory."""
        self.data.evaluation = evaluation


# template = """This is a conversation to collect and evaluate a company's general overview. The chatbot is designed to be informative and engaging. Your objetive is to assist me in creating
# a good company general overview. Start the conversation with "Here is the current company profile:" to present the current general overview and then followed by communicating based on evaluation.
# The communication should either ask for additional information or confirmation based on evaluation.

# Previous conversation history:
# {conversation_history}

# Current general overview:
# {general_overview}

# Overview evaluation:
# {general_overview_evaluation}

# Conversation:
# Human: {input}
# AI:
# """

template = """This is a conversation to communicate with user to get a satisfied company profile. The chatbot is designed to be informative and engaging. 
Your objetive is to either ask for confirmation or additional information based on evaluation.

## Response should be in two paragraphs:
1. Always start the conversation with "Here is the current company profile:" to present the current aspect of comapny profile.
2. Then communicate with user. If evaluation suggests satisfied, ask for confirmation. Otherwise, ask for additional information.

Previous conversation history:
{conversation_history}

Current aspect of comapny profile:
{aspect}

Overview evaluation:
{evaluation}

Conversation:
Human: {input}
AI:
"""

prompt = PromptTemplate(
    input_variables=[
        "conversation_history",
        "aspect",
        "evaluation",
        "input",
    ],
    template=template,
)

custom_memory = CustomConversationMemory()

chatbot_chain = ConversationChain(
    llm=llm, prompt=prompt, verbose=True, memory=custom_memory
)
