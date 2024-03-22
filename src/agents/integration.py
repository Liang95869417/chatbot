from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.llm_providers.chat_model_provider import llm, llm4
from langchain_core.output_parsers import StrOutputParser



# create a agent to integrate user information with current aspect
system_prompt = """
Merge the current aspect of the company profile with the additional information provided by the user.
The output should solely focus on incorporating and updating the company profile with the new information. Ensure the revised profile is coherent, comprehensive, and free from any details not directly related to the company's profile.

Response Guidelines:
Integrate Thoroughly: Carefully weave the user-provided additional information into the existing company profile, ensuring the updated profile is seamless and includes all relevant details.
Maintain Relevance: Ensure every piece of information in the updated profile is pertinent to the company's profile. Exclude any content that does not directly relate to or enhance understanding of the company.
Clarity and Coherence: Present the updated company profile in a clear and structured manner. It should be easy for the reader to understand the company's current state, including any new developments or changes highlighted by the user.
No Meta Commentary: Refrain from commenting on the quality of the update or the integration process. The focus should be entirely on delivering the updated company profile content.
"""

human_prompt = """Generate updated company profile aspect by integrating User-Provided additional information.
Previous Company Profile Aspect::
{aspect}
User-Provided additional information:
{add_info}
"""

sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
email_generate_human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages(
    [sys_prompt, email_generate_human_message]
)

integration_chain = chat_prompt | llm | StrOutputParser()
