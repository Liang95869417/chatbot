from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm, llm4


system_prompt = "As an analyst, your task is to assess the given general overview based on the specified criteria."
human_prompt = """Please evaluate the general overview according to the following criteria:
% Criteria:
- Obtain fundamental information about the company, which may include its name, industry, products or services, unique attributes, target market, and notable achievements or innovations.

Based on your evaluation, if the overview does not sufficiently meet the criteria, please specify what additional information is required by asking targeted questions.

% Here is General Overview to evaluate:
{general_overview}

% OUTPUT FORMAT:
{output_format}
"""
evaluation_parser = OutputFixingParser.from_llm(
    parser=PydanticOutputParser(pydantic_object=EvaluationOutput), llm=llm
)
sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages(
    [sys_prompt, human_message]
).partial(output_format=evaluation_parser.get_format_instructions())


overview_evaluation_chain = chat_prompt | llm | evaluation_parser
