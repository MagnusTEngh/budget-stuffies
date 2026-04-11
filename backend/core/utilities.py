import logging

from pathlib import Path

logger = logging.getLogger(__name__)

def find_project_root():
    project_root = next(
        p for p in Path(__file__).parents if (p / ".git").exists()
    )
    logger.debug(project_root)
    return project_root