from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from src.llm_providers.chat_model_provider import llm
from pydantic import BaseModel, Field


response_schemas = [
    ResponseSchema(name="intent", description="user's intent"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


system_prompt = """Given a user's message, classify the intent as either 'Accept Information' or 'Add More Information'.

If the user's message indicates satisfaction with the current aspect of the profile, classify it as 'Accept Information'.

If the user's message suggests they want to provide additional details or corrections, classify it as 'Add More Information'.
"""
human_prompt = """Determine the intent of the following message:
{user_message}

Is the user accepting the current information or adding more details?
{format_instructions}
"""
sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages([sys_prompt, human_message]).partial(
    format_instructions=output_parser.get_format_instructions()
)

intent_recognition_chain = chat_prompt | llm | output_parser
