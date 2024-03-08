from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from src.llm_providers.chat_model_provider import llm, llm4


response_schemas = [
    ResponseSchema(name="intent", description="user's intent"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


system_prompt = """
Reevaluate the user's message to accurately determine their intention. If the message explicitly conveys satisfaction, approval, or contentment with their profile, classify it as 'Accept Information'. Exercise caution with messages lacking these explicit expressions, as they may indicate a desire to provide more details or corrections. Even if the message seems detailed or positive, unless it directly states satisfaction or approval, consider categorizing the intent as 'Add More Information'. Your goal is to identify the user's intention accurately by examining both explicit affirmations of satisfaction and potential implicit cues hinting at the need for additional information.
"""

human_prompt = """Your goal is to determine the intent behind the user's message:
{user_message}

Is the user expressing acceptance of the current information, or are they providing additional details?
{format_instructions}
"""

sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages([sys_prompt, human_message]).partial(
    format_instructions=output_parser.get_format_instructions()
)

intent_recognition_chain = chat_prompt | llm | output_parser
