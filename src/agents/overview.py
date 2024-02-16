from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm


system_prompt = """You are an analyst to evaluate company overview based on following criteria. The repsonse should always be polite and to the point.

##Criteria:
1. Important to follow user's intention
2. Gather basic information about the company, possibly including its name, industry, products or services, unique features, target market, and any notable achievements or innovations.
"""
human_prompt = """Evaluate the following general_overview: 
{general_overview}
%OUTPUT FORMAT:
{output_format}
"""
evaluation_parser = OutputFixingParser.from_llm(
    parser=PydanticOutputParser(pydantic_object=EvaluationOutput), llm=llm
)
sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
email_generate_human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages(
    [sys_prompt, email_generate_human_message]
).partial(output_format=evaluation_parser.get_format_instructions())


overview_evaluation_chain = chat_prompt | llm | evaluation_parser
