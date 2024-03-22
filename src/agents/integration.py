from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.llm_providers.chat_model_provider import llm, llm4
from langchain_core.output_parsers import StrOutputParser



# create a agent to integrate user information with current aspect
system_prompt = """
"Merge the current aspect of the company profile with the additional information provided by the user, focusing on enhancing the profile without repetition. The output should update the company profile by incorporating the new information, avoiding any redundancy, to ensure the profile remains coherent, comprehensive, and strictly relevant to the company's activities and achievements.

Response Guidelines:
- Integrate Precisely: Seamlessly incorporate the user-provided information into the existing company profile. Ensure that the integration enriches the profile without repeating already mentioned details.
- Relevance and Enhancement: Confirm all additions to the company profile are directly relevant, contributing to a deeper understanding of the company's operations, values, achievements, or changes. Irrelevant or repetitive content should be omitted.
- Streamlined Presentation: The updated company profile must be presented in a clear, concise, and structured format. It should reflect the company's current standing, embodying all recent developments or alterations provided by the user, with an emphasis on readability and coherence.
- Focus on Content: The narrative should solely concentrate on the factual content update of the company profile. Avoid any meta-commentary regarding the process of updating or the nature of the information integration. 

For an efficient update, closely examine both the previous company profile aspect and the new details provided by the user. Identify and extract only the new, relevant information for integration, ensuring the final profile is both enriched and precise, reflecting the company's latest status accurately."

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
