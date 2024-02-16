import os
from typing import Union
from langchain_community.chat_models import ChatOllama
from langchain_openai import AzureChatOpenAI
from config import Settings



class ChatModelProvider:
    @staticmethod
    def get_chat_model(
        model_name: str, **model_kwargs
    ) -> Union[ChatOllama, AzureChatOpenAI]:
        if model_name in ["GPT-Turbo", "GPT-4", "GPT-35-turbo-16k", "GPT-4-Turbo"]:
            return AzureChatOpenAI(**model_kwargs, deployment_name=model_name)
        else:
            raise ValueError(f"Model {model_name} not supported")


settings = Settings()
# azure_model_args = {
#     "azure_endpoint": "https://intelligestsweeden.openai.azure.com/",
#     "openai_api_version": "2023-07-01-preview",
#     "openai_api_key": "788ad89e136d45dc949ef9b84ee0f541",
#     "openai_api_type": "azure",
#     "temperature": 0.0,
# }
azure_model_args = {
    "azure_endpoint": settings.base_url,
    "openai_api_version": settings.api_key,
    "openai_api_key": settings.api_key,
    "openai_api_type": settings.api_type,
    "temperature": 0.0,
}
llm = ChatModelProvider.get_chat_model("GPT-Turbo", **azure_model_args)
