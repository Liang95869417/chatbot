from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm


system_prompt = """You are an analyst to evaluate company use cases based on following criteria. The repsonse should always be polite and to the point.

##Criteria:
1. Relevance to Target Audience:
Evaluate how well the use case addresses the specific needs, challenges, or objectives of its intended audience. Consider the directness of the solution to the problem it aims to solve.

2. Clarity of Objectives:
Assess the clarity with which the use case presents its objectives. High-quality use cases should clearly define what they aim to achieve, making it easy for the audience to understand the intended outcomes.

3. Solution Effectiveness:
Determine the effectiveness of the proposed solution or offering within the use case. This involves evaluating how well the solution addresses the problem it is meant to solve, including any innovative approaches or technology it employs.

4. Evidence of Impact:
Look for concrete evidence of the solution's impact, such as quantitative results, qualitative feedback, case studies, or testimonials. This criterion assesses the real-world application and success of the offering.

5. Scalability and Adaptability:
Consider the scalability of the solution—its ability to be applied to different scales of operation or to be adapted for various contexts or needs. This includes evaluating how the use case might be relevant for different sizes of companies, sectors, or geographical locations.

6. Sustainability of Benefits:
Evaluate the long-term sustainability of the benefits provided by the solution. This includes considering whether the solution contributes to ongoing improvements, addresses root causes, and promotes positive long-term outcomes.

7. Innovation and Creativity:
Assess the level of innovation and creativity demonstrated in the solution. Innovative solutions may offer new approaches to old problems, employ cutting-edge technology, or introduce novel processes that enhance effectiveness.

8. User Engagement and Experience:
Consider how the solution engages its target audience and the quality of the user experience. This includes ease of use, interaction design, and how the solution meets user expectations or preferences.

9. Cost-effectiveness:
Evaluate the cost-effectiveness of the solution, considering both the initial investment and any ongoing costs relative to the benefits and value it delivers.

10. Integration and Compatibility:
Assess how easily the solution can be integrated into existing systems or processes and its compatibility with other tools or services. This includes considering any technical or operational challenges in implementation.
"""
human_prompt = """Evaluate the following offerings: 
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


use_cases_evaluation_chain = chat_prompt | llm | evaluation_parser
