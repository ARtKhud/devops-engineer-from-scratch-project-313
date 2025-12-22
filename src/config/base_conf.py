from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    PROJECT_NAME: str = "devops-engineer-from-scratch"
    VERSION: str = "1.0.0"
