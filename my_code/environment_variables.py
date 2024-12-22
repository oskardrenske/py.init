import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

load_dotenv(find_dotenv())


# strings meet the condition of True if they have content.
# A comparion of the lower-case-converted string to "true" gives us a boolean value.


def read_bool_env_var(env_var_name: str) -> bool:
    var = os.getenv(env_var_name, default="").lower().strip()
    result = var in ["true", "yes", "y", "1"]
    logger.debug(f"Environment variable {env_var_name} was {result}")
    return result


# an alternative:
my_bool_env_var = os.getenv("MY_BOOL_ENV_VAR", "").lower().strip() == "true"


my_string_env_var = os.getenv("MY_ENV_VAR", "default value")


my_bool_env_var_2 = read_bool_env_var("MY_BOOL")

logger.info("Loaded environment variables")
