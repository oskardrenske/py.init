import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

my_string_env_var = os.getenv("MY_ENV_VAR", "default value")

# strings meet the condition of True if they have content.
# A comparion of the lower-case-converted string to "true" gives us a boolean value.
my_bool_env_var = os.getenv("MY_BOOL_ENV_VAR", "").lower() == "true"


def main():
    print(my_string_env_var)
    print(my_bool_env_var)


if __name__ == "__main__":
    main()
