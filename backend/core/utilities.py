import logging
import requests
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


def external_request(method, url, **kwargs):
    """
    Generic HTTP request wrapper.

    :param method: HTTP method as string ("GET", "POST", etc.)
    :param url: Request URL
    :param kwargs: Passed directly to requests.request()
    :return: response object if status_code == 200
    :raises: requests.HTTPError or ValueError
    """
    try:
        response = requests.request(method=method, url=url, **kwargs)

        response.raise_for_status()
        return response
    except Exception as e:
        logger.error(e, exc_info=True)
