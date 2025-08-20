from pydantic import BaseSettings

class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = "sqlite:///./laxis_agent.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/oauth2callback"

    # Microsoft OAuth
    MS_CLIENT_ID: str = ""
    MS_CLIENT_SECRET: str = ""
    MS_REDIRECT_URI: str = "http://localhost:8000/ms_oauth2callback"

    class Config:
        env_file = ".env"   

settings = Settings()
