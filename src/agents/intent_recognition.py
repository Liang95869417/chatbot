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


system_prompt = """Refine your analysis of the user's message to accurately identify their intent. Classify the message as 'Accept Information' only if it explicitly expresses satisfaction, approval, or contentment with the current aspect of their profile.

However, treat any message lacking these explicit expressions of satisfaction with caution. Even if the message appears detailed or positive, unless it directly states satisfaction or approval, it may indicate that the user intends to provide additional details or corrections. In such instances, classify the intent as 'Add More Information'.

Your task is to discern the user's intent with precision, considering both explicit affirmations of satisfaction and the potential for implicit cues suggesting the desire to add more information.
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
