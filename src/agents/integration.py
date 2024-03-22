from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from src.llm_providers.chat_model_provider import llm, llm4
from langchain_core.output_parsers import StrOutputParser



# create a agent to integrate user information with current aspect
system_prompt = """
Based on the update_mode parameter, either merge the current aspect of the company profile with additional information provided by the user or remove outdated information, focusing on enhancing or streamlining the profile accordingly. When the update_mode is 'addition', incorporate the new information, avoiding any redundancy, to ensure the profile remains coherent, comprehensive, and strictly relevant to the company's activities and achievements. When the update_mode is 'removal', identify and omit any outdated or redundant details, ensuring the profile accurately reflects the company's current state.

Response Guidelines:
- Adapt to Update Mode: If the update_mode is 'addition', seamlessly incorporate user-provided information into the existing company profile to enrich it without repetition. If the update_mode is 'removal', carefully identify and exclude any outdated or redundant information.
- Relevance and Enhancement: Ensure all changes to the company profile are directly relevant, either by adding new insights or removing obsolete information, contributing to a clearer understanding of the company's operations, values, achievements, or changes.
- Streamlined Presentation: Present the updated company profile in a clear, concise, and structured format, reflecting the company's current standing with an emphasis on readability and coherence.
- Focus on Content: Concentrate solely on the factual content update of the company profile, avoiding any meta-commentary regarding the process of updating or the nature of the information integration.

For an efficient update, closely examine both the previous company profile aspect and the new details or identified redundancies. Modify the profile to reflect the company's latest status accurately, based on the update_mode parameter.

"""

human_prompt = """Generate updated company profile aspect by integrating or removing information based on the provided update_mode.
Previous Company Profile Aspect:
{aspect}
User-Provided additional information (for 'addition') or Information to Remove (for 'removal'):
{update_info}
Update Mode: {update_mode}
"""

sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
email_generate_human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages(
    [sys_prompt, email_generate_human_message]
)

integration_chain = chat_prompt | llm | StrOutputParser()
