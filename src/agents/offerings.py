from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm, llm4


system_prompt = """
Please provide an evaluation of the company offerings based on the following criteria. Your response should be polite and concise.

## Criteria:
1. Core Offerings:
- Description: Provide an overview of the primary products or services offered by the company, emphasizing their key functions and intended use.
- Target Market: Specify the specific audience or sector (e.g., commercial, residential, healthcare) for which the offerings are tailored.
- Application: Illustrate how the products or services are utilized in real-world scenarios, showcasing practical use cases.

2. Unique Features:
- Innovation: Highlight any innovative aspects of the offerings that differentiate them from competitors, such as proprietary technology or unique service models.
- User Experience: Describe features that enhance user experience, including ease of use, accessibility, and interaction design.
- Integration and Compatibility: Explain how the offerings seamlessly integrate with existing systems or platforms and their compatibility with other products or services.

3. Benefits:
- Efficiency and Productivity: Discuss how the offerings enhance efficiency or productivity for users or businesses.
- Security and Reliability: Detail the security features and reliability measures that ensure the safety and dependability of the offerings.
- Cost-Effectiveness: Evaluate the cost-effectiveness of the offerings, including potential long-term savings and return on investment.
"""

human_prompt = """
Please evaluate the following offerings:
{offerings}
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


offerings_evaluation_chain = chat_prompt | llm | evaluation_parser
