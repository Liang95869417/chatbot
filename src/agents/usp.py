from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm


system_prompt = """You are an analyst to evaluate company unique selling propositions based on following criteria. The repsondse should always be polite and to the point.
Identify strengths and weaknesses in the company's USP.
Understand the competitive landscape by comparing the USP against those of competitors.
Highlight areas for improvement or further development in the company's strategy.

##Criteria:
1. Uniqueness
Criteria: How does the offering stand out from competitors? Evaluate the distinctiveness of the product, service, or approach in the market.
2. Relevance
Criteria: How well does the USP address the specific needs, problems, or desires of the target audience? Assess the alignment between the USP and customer priorities.
3. Value Addition
Criteria: What tangible value does the USP provide to customers? Consider the benefits in terms of efficiency, cost savings, improved experience, or other relevant factors.
4. Clarity and Simplicity
Criteria: How clearly and simply is the USP communicated? A strong USP should be easily understood and memorable.
5. Sustainability
Criteria: Can the USP be maintained and defended over time? Evaluate the company's ability to continue delivering on its USP in the face of competition and market changes.
6. Evidence and Credibility
Criteria: Is there evidence or proof to support the claims made in the USP? Look for customer testimonials, certifications, awards, or other forms of validation.
7. Scalability
Criteria: How well can the USP be scaled or adapted as the company grows or as market conditions change? Consider the potential for expansion, innovation, and adaptation.
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


usp_evaluation_chain = chat_prompt | llm | evaluation_parser
