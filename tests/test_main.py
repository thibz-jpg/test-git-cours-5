import pytest

from src.main import get_meaning_of_life


@pytest.mark.parametrize(
    "question,expected",
    [
        ("What is the meaning of life?", 42),
        ("Tell me about LIFE please", 42),
        ("life", 42),
        ("LIFE", 42),
        ("What's the purpose of life in the universe?", 42),
        ("Why does life exist?", 42),
        ("   What is the meaning of    LiFe    ?", 42),
    ],
)
def test_valid_life_questions(question, expected):
    """Test that questions containing 'life' return 42"""
    result = get_meaning_of_life(question)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_question",
    [
        "What is love?",
        "Why is the sky blue?",
        "How many stars are there?",
        "Tell me about the universe",
        "",
        "   ",
    ],
)
def test_invalid_questions(invalid_question):
    """Test that questions without 'life' raise ValueError"""
    with pytest.raises(ValueError) as exc_info:
        get_meaning_of_life(invalid_question)

    assert str(exc_info.value) == "Question not deep enough"
