import os

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

settings = Settings()

# Optional: sanity check at startup
if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables!")
