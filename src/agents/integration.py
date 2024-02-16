from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.llm_providers.chat_model_provider import llm
from langchain_core.output_parsers import StrOutputParser



# create a agent to integrate user information with current aspect
system_prompt = """You are an analyst to integrate current aspect of company profile with additional information from user. """
human_prompt = """Here is current aspect of company profile: 
{aspect}
Here is additional information:
{add_info}
"""

sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
email_generate_human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages(
    [sys_prompt, email_generate_human_message]
)

integration_chain = chat_prompt | llm | StrOutputParser()
