import os
import yaml
from pathlib import Path
from typing import Literal, Optional
import copy
from dotenv import load_dotenv


load_dotenv()  # must come before reading env vars

BASE_PATH = Path(__file__).parent
GLOBAL_CONFIG = BASE_PATH / "application.yaml"
PROFILE_CONFIGS = {
    "dev": BASE_PATH / "application-dev.yaml",
    "prod": BASE_PATH / "application-prod.yaml",
}

Profile = Literal["dev", "prod"]

def load_yaml(file_path: Path) -> dict:
    if not file_path.exists():
        return {}
    with file_path.open("r") as f:
        return yaml.safe_load(f) or {}

def merge_dicts(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def get_active_profile() -> Profile:
    # Default to 'dev' if not set
    profile = os.environ.get("APP_PROFILE", "dev").lower()
    if profile not in PROFILE_CONFIGS:
        raise ValueError(f"Invalid APP_PROFILE: {profile}. Must be one of {list(PROFILE_CONFIGS.keys())}")
    return profile  # type: ignore

def load_config(profile: Optional[Profile] = None) -> dict:
    if profile is None:
        profile = get_active_profile()

    global_config = load_yaml(GLOBAL_CONFIG)
    profile_config = load_yaml(PROFILE_CONFIGS[profile])
    app_config = merge_dicts(global_config, profile_config)
    return app_config

APP_CONFIG = load_config()
