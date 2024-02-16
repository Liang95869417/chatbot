from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from src.models.evaluation_output import EvaluationOutput
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from src.llm_providers.chat_model_provider import llm
from langchain.tools import BaseTool


class OverviewEvaluationTool(BaseTool):
    name = "Overview Evaluation"
    description = "use this tool when given company overview to evaluate."

    def _run(self, general_overview: str):
        system_prompt = """You are an analyst to evaluate company overview based on following criteria. The repsond should always be polit and to the point.

        ##Criteria:
        1. Important to follow user's intention
        2. Gather basic information about the company, including its name, industry, products or services, unique features, target market, and any notable achievements or innovations.
        3. If available, also include the company's mission statement, key benefits of their products or services, and how they adapt to market trends or customer needs.
        
        ##You should react in two formats: 
        1. If input is not a valid company overview about a company. Then guide the user collect company overview with a list of questions.
        2. If input is a valid company overview about a company. Then either ask for confirmation or additional information.
        """
        human_prompt = """Evaluate the following general_overview: 
        {general_overview}

        Response should contain two parts: original aspect of company profile and evaluation result separated by "\n". If input is not a valid company overview about a company, the first part should be "There is no company overview collected in our database".
        """
        sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
        email_generate_human_message = HumanMessagePromptTemplate.from_template(
            human_prompt
        )
        chat_prompt = ChatPromptTemplate.from_messages(
            [sys_prompt, email_generate_human_message]
        )

        prompt_variables = {"general_overview": general_overview}

        chain = chat_prompt | llm | StrOutputParser()
        output = chain.invoke(prompt_variables)
        print("outpput type from OverviewEvaluationTool", type(output))
        return output

    def _arun(self, general_overview: str):
        raise NotImplementedError("This tool does not support async")


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
