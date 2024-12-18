import pytest

"""
Test can use Pytest fixtures that are automagically imported from conftest.py

fixtures are called by name only, not as functions (i.e. no parenthesis)
fixtures can be written in the test file if they are very specific and not used elsewhere
"""


def test_simple():
    assert True


def test_with_fixture(setup_and_teardown):
    print("test")


def test_big_data(load_test_data):
    """
    Load test data once in a fixture for all tests (if it's an expensive operation)
    """
    print(load_test_data)


def test_compare_singletons(setup_and_teardown):
    """
    comparisions with True, False or None should be done with 'is' not with '==' (but it works with ==)
    """
    test_data = "this is my test data"
    assert test_data is not None
    assert test_data is not False
    assert test_data  # string with content is True, but it isn't the singelton True


def test_expected_error():
    test_data = "this is my test data"
    with pytest.raises(AssertionError):
        """
        using with pytest.raises(AssertionError) will swallow the AssertionError but will fail if an other 
        (or no exception at all) is raised.
        The alternative would be a long try-except-except-else clause
        """
        assert test_data == "hello world"


@pytest.mark.parametrize("param", ["a", "b"])
def test_parametrized(param, setup_and_teardown):
    print(param)


def test_without_fixture():
    print("You don't have to use fixtures ")


def test_if_something_in_str():
    test_data = "this is my test data"
    assert "my" in test_data


def test_if_something_in_list():
    test_data = [1, 2, 3, 4]
    assert 3 in test_data
    # use sets if there is a lot of data, much faster
