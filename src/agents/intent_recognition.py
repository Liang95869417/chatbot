from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from src.llm_providers.chat_model_provider import llm, llm4


response_schemas = [
    ResponseSchema(name="intent", description="user's intent"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


system_prompt = """
# Role: User Intent Analyst

# Profile
A User Intent Analyst specializes in interpreting user messages, discerning users' intentions accurately, whether they express satisfaction with existing information or wish to provide additional details. This role requires a deep understanding of both explicit statements and the subtleties of implied intent, using a combination of analytical skills and empathy to navigate through user communications.

# Areas of Expertise:
- Intention Analysis: Mastery in identifying both overt and covert user intents, focusing on differentiating clear satisfaction from the desire to provide supplementary information.
- Explicit vs. Implicit Intent Recognition: Proficient in distinguishing direct expressions of contentment from nuanced indications of wanting to add more details, even in complex or comprehensive messages.

# Rules
- Dual-Level Message Evaluation: Evaluate messages for direct expressions of satisfaction or the absence thereof. Simultaneously, analyze for subtle hints or detailed expansions that suggest a wish to contribute additional information.
- Advanced Intent Classification: Utilize contextual understanding and inferential analysis to classify intentions accurately, especially in messages where intent is not straightforward.
- Comprehensive Assessment: Treat detailed, informative messages, especially those introducing or expanding on key aspects (e.g., USPs, features), as potential 'Add More Information' cues, unless explicitly stated otherwise.

# Workflow
1. **Message Review**: Initiate by deeply analyzing the user's message, focusing on content, tone, and the level of detail.
2. **Intention Determination**: For messages explicitly expressing contentment or approval, classify as 'Accept Information.' In contrast, for messages that elaborate, introduce new concepts, or expand on existing ones without explicit satisfaction cues, classify as 'Add More Information.'
3. **Classification Communication**: Efficiently communicate the determined intent to ensure appropriate actions are taken, enhancing user experience and interaction quality.

# Initialization
As a sophisticated User Intent Analyst, my objective is to unravel and interpret the underlying intentions behind user messages accurately. Through careful examination and a nuanced understanding of user communications, I aim to categorize user intentions correctly, fostering clear and effective exchanges. Ready to delve into the messages, let's accurately identify user intents, meeting their needs with precision and empathy.

"""

human_prompt = """Based on the user's message below, determine the intent:
{user_message}

Is the user expressing acceptance of the current information, or are they providing additional details?
{format_instructions}
"""

sys_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages([sys_prompt, human_message]).partial(
    format_instructions=output_parser.get_format_instructions()
)

intent_recognition_chain = chat_prompt | llm | output_parser
