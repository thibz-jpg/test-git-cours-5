import argparse
from typing import Union

from src.utils import logger


def get_meaning_of_life(question: str) -> Union[int, str]:
    """Returns the answer to life, universe and everything.

    Args:
        question: An existential question

    Returns:
        42 if the question is about life, error message otherwise
    """
    if "life" in question.lower():
        return 42

    raise ValueError("Question not deep enough")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the meaning of life")
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        default="What is the meaning of life?",
        help="An existential question",
    )
    args = parser.parse_args()

    logger.glitch(f"Reflecting on question 🧠: {args.question}")
    result = get_meaning_of_life(args.question)
    logger.success(f"The answer is {result}")
