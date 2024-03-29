from typing import Union
from langchain_community.chat_models import ChatOllama
from langchain_openai import AzureChatOpenAI
from config import Settings
import os


class ChatModelProvider:
    @staticmethod
    def get_chat_model(
        model_name: str, **model_kwargs
    ) -> Union[ChatOllama, AzureChatOpenAI]:
        if model_name in ["GPT-Turbo", "GPT-4", "GPT-35-turbo-16k", "GPT-4-Turbo"]:
            if os.environ["FASTAPI_ENVIRONMENT"] == "dev":
                return AzureChatOpenAI(**model_kwargs, deployment_name="GPT-Turbo")
            else:
                return AzureChatOpenAI(**model_kwargs, deployment_name=model_name)
        else:
            raise ValueError(f"Model {model_name} not supported")


settings = Settings()
azure_model_args = {
    "azure_endpoint": settings.base_url,
    "openai_api_version": settings.api_version,
    "openai_api_key": settings.api_key,
    "openai_api_type": settings.api_type,
    "temperature": 0.0,
}
if os.environ["FASTAPI_ENVIRONMENT"] == "dev":
    llm = ChatModelProvider.get_chat_model("GPT-Turbo", **azure_model_args)
    llm4 = ChatModelProvider.get_chat_model("GPT-4", **azure_model_args)
else:
    llm = ChatModelProvider.get_chat_model("GPT-Turbo", **azure_model_args)
    llm4 = ChatModelProvider.get_chat_model("GPT-4", **azure_model_args)