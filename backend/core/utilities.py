import logging

from pathlib import Path

logger = logging.getLogger(__name__)

def find_project_root():
    project_root = next(
        p for p in Path(__file__).parents if (p / ".git").exists()
    )
    logger.debug(project_root)
    return project_root

def required_env(variable_name):
    value = os.getenv(variable_name)
    if value is None:
        raise ValueError(f"{variable_name} is required")
    return value