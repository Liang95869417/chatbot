from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm, llm4


system_prompt = """As an analyst responsible for evaluating a company's unique selling propositions, your task is to thoroughly assess the strengths and weaknesses of the USP using the following criteria:

1. Uniqueness: Evaluate how the company's offering differentiates itself from competitors in terms of product, service, or market approach.
2. Relevance: Analyze how effectively the USP meets the specific needs, problems, or desires of the target audience and aligns with customer priorities.
3. Value Addition: Consider the concrete value that the USP delivers to customers in terms of efficiency, cost savings, enhanced experience, or other pertinent factors.
4. Clarity and Simplicity: Evaluate how clearly and simply the USP is communicated to ensure it is easily understood and memorable.
5. Sustainability: Assess the company's ability to uphold and defend the USP over time amidst competition and market fluctuations.
6. Evidence and Credibility: Look for supporting evidence or validation, such as customer testimonials, certifications, awards, to substantiate the claims made in the USP.
S7. calability: Consider how well the USP can be expanded or adjusted as the company grows or as market conditions evolve, including potential for innovation and adaptation.

Your analysis should pinpoint areas for enhancement or further development in the company's strategy, while maintaining a respectful and concise manner.
"""
human_prompt = """Evaluate the following unique selling points: 
{unique_selling_points}

Based on your evaluation, if the unique selling points does not sufficiently meet the criteria, please specify what additional information is required by asking targeted questions.

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


usp_evaluation_chain = chat_prompt | llm | evaluation_parser
