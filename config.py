import os
from dotenv import load_dotenv
load_dotenv()


class Settings:
    WORKFLOW_NAME: str = "run-dyson-run"
    OWNER: str = "mertguvencli"
    REPO: str = "custom-tracker"
    GH_TOKEN: str = os.getenv("GITHUB_TOKEN")
    PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
    PUSHOVER_USER = os.getenv("PUSHOVER_USER")


settings = Settings()
