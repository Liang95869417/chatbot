from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    atlas_uri: str
    database_name: str
    api_type: str
    base_url: str
    api_key: str
    api_version: str
    redirect_url: str
    jwt_secret: str
    jwt_algorithm: str
    company_settings_return_url: str
    card_crm_return_url: str
    zyte_api_key: str
    zyte_endpoint: str
    mixpanel_token: str
    langchain_tracing_v2: str
    langchain_endpoint: str
    langchain_api_key: str
    langchain_project: str
    model_config = SettingsConfigDict(env_file=".env.dev")
