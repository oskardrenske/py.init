from pydantic import ValidationError
import pytest

from my_code.my_validated_code import Init, Name, StringOrNone, Numbers

"""
Pydantic-classer måste instantieras med namngivna argument

Not OK: Name("Oskar")
OK:     Name(name="Oskar)
Annars: TypeError: BaseModel.__init__() takes 1 positional argument but 3 were given

"""


def test_init():
    Init(name="demo name")


def test_user():
    Name(name="A")


@pytest.mark.parametrize("name", [1, None, True, False, [], ["name"], {}, {"name": "Oskar"}, Name])
def test_name_fail(name):
    with pytest.raises(ValidationError):
        Name(name=name)


def test_number_fail():
    with pytest.raises(ValidationError):
        # this will raise a ValidationError because you send strings
        #  when ints are expected. If not, the test fail.
        Numbers(arg_1="1", arg_2="2")


def test_numbers_OK():
    Numbers(arg_1=1, arg_2=2)


@pytest.mark.parametrize("var", ["hello", None])
def test_optional_none(var):
    StringOrNone(var=var)


def test_class_to_json():
    numbers = Numbers(arg_1=10, arg_2=20)
    numbers_json = numbers.model_dump_json()
    assert numbers_json == '{"arg_1":10,"arg_2":20}'
