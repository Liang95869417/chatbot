# Swayle Virtual SDR Chatbot

The Swayle Virtual SDR (Sales Development Representative) Chatbot is an automated system designed to assist companies in crafting and refining their profiles in the Swayle services. Utilizing publicly available information and interactive dialogue, the chatbot enables users to review, update, and optimize various aspects of their company profile, including general overview, offerings, unique selling propositions, and customer success stories.

## Features

- **Automated Profile Drafting**: Generates preliminary company profiles using publicly available data.
- **Interactive Refinement**: Facilitates user-driven profile refinement through a conversational interface.
- **Aspect Evaluation**: Analyzes and suggests improvements for different profile aspects.
- **Intent Recognition**: Understands user intent to add information or accept current content.

## To run the chatbot:

```
python main.py
```

## Project Structure
```
chatbot/
│
├── src/
|   |── agents/
|   |   |── __init__.py
|   |   |── integration.py
|   |   |── intent_recognition.py
|   |   |── interaction.py
|   |   |── offerings.py
|   |   |── overview.py
|   |   |── use_cases.py
|   |   └── usp.py
|   
|   |── db/
|   |   |── __init__.py
|   |   └── db_handler.py
|
|   |── llm_provider/
|   |   |── __init__.py
|   |   └── chat_model_provider.py
|
|   |── models/
|   |   |── __init__.py
|   |   └── evaluation_output.py
|
│   ├── __init__.py
│   ├── chatbot.py
│   └── utils.py
│
├── .env.dev
├── requirements.txt
├── test_chain.py
└── README.md
```

