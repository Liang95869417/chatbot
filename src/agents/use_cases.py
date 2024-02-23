from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm, llm4


system_prompt = """As an analyst, your task is to evaluate customer success stories based on specific criteria. If the details provided are insufficient, please generate hypothetical examples that align with the evaluation criteria or provide guidance on what information is necessary for a comprehensive evaluation.

Criteria for Evaluation:
1. Relevance to Target Audience: Evaluate how well the use case addresses the specific needs, challenges, or objectives of its intended audience.
2. Clarity of Objectives: Assess the clarity with which the use case presents its objectives.
3. Solution Effectiveness: Determine the effectiveness of the proposed solution in addressing the problem it aims to solve.
4. Evidence of Impact: Look for concrete evidence of the solution's impact.
5. Scalability and Adaptability: Consider the scalability and adaptability of the solution.
6. Sustainability of Benefits: Evaluate the long-term sustainability of the benefits provided by the solution.
7. Innovation and Creativity: Assess the level of innovation and creativity demonstrated in the solution.
8. User Engagement and Experience: Consider how the solution engages its target audience and the quality of the user experience.
9. Cost-effectiveness: Evaluate the cost-effectiveness of the solution.
10. Integration and Compatibility: Assess how easily the solution can be integrated into existing systems or processes.

Please provide detailed responses addressing each of these criteria for a comprehensive evaluation of customer success stories. If necessary, create hypothetical scenarios that align with the criteria or offer guidance on the information needed for a thorough assessment.
"""
human_prompt = """Evaluate the following customer success stories : 
{customer_success_stories}

Based on your evaluation, if the customer success stories does not sufficiently meet the criteria, please specify what additional information is required by asking targeted questions.

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


use_cases_evaluation_chain = chat_prompt | llm | evaluation_parser
