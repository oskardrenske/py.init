import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

load_dotenv(find_dotenv())

"""
Strings meet the condition of True if they have content.
A comparion of the lower-case-converted string to "true" or other known "truthish" values gives us a boolean value.
distutils, which was removed in 3.12, had a strtobool function. 
https://github.com/python/cpython/blob/v3.11.2/Lib/distutils/util.py#L308
"""


def read_bool_env_var(env_var_name: str) -> bool:
    var = os.getenv(env_var_name, default="").lower().strip()
    result = var in ["true", "yes", "y", "1"]
    logger.debug(f"Environment variable {env_var_name} was {result}")
    return result


# an alternative:
# convert to lower case and compare to the string "true". The comparison result is the bool variable.
my_bool_env_var = os.getenv("MY_BOOL_ENV_VAR", "").lower().strip() == "true"


my_bool_env_var_2 = read_bool_env_var("MY_BOOL")

logger.info("Loaded environment variables")
