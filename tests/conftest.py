import pytest
from loguru import logger

# https://docs.pytest.org/en/stable/how-to/fixtures.html


@pytest.fixture
def setup_and_teardown():
    """
    Doing setup
    Handing over control to the calling test
    Doing teardown
    Using default scope "function" so that it is called for every test
    """
    logger.info("Setting up test")
    yield  # handing over to the test that use this fixture
    logger.info("Teardown after test")


@pytest.fixture(scope="session")
def load_test_data():
    """
    An expensive operation that is done once for all tests,
    scope="session" means it just runs once for every test run (which could be one or many tests)
    """
    return "some big data"
