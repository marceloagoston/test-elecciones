import pytest
from datetime import date

from voting.utils import has_voted, has_voted_percentage, can_vote
from .factories import VoterFactory


# has_voted tests
@pytest.mark.django_db
@pytest.mark.parametrize(
    'has_voted_value, expected_result',
    [
        (True, True),  # Test case for has_voted=True
        (False, False),  # Test case for has_voted=False
    ],
)
def test_has_voted(has_voted_value, expected_result):
    voter = VoterFactory(has_voted=has_voted_value)

    assert has_voted(voter.dni) == expected_result


@pytest.mark.django_db
def test_has_voted_not_exits():
    assert has_voted(1234) is None


# has_voted_percentage tests
@pytest.mark.django_db
@pytest.mark.parametrize(
    'voters_data, expected_percentage',
    [
        ([], 0),  # Test case for 0 voters
        ([(True, 1), (True, 2), (True, 3), (True, 4)], 100),  # Test case for all voters voted
        ([(True, 1), (True, 2), (False, 3), (False, 4)], 50),  # Test case for 50-50
    ],
)
def test_has_voted_percentage(voters_data, expected_percentage):
    for voted, dni in voters_data:
        VoterFactory(has_voted=voted, dni=dni)

    voted_percentage = has_voted_percentage()

    assert voted_percentage == pytest.approx(expected_percentage, abs=0.01)


# Birth date Test
@pytest.mark.django_db
@pytest.mark.parametrize(
    'birth_date, expected_result',
    [
        (date(1991, 1, 1), True),  # Test case para una persona mayor de edad
        (date(2010, 1, 1), False),  # Test case para una persona menor de edad
        (
            date.today(),
            False,
        ),  # Test case para una persona que acaba de nacer (siempre debe fallar)
    ],
)
def test_is_adult(birth_date, expected_result):
    voter = VoterFactory(birth_date=birth_date)

    assert can_vote(voter.birth_date) == expected_result
