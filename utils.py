def split_ingredients(ingredients: str) -> list:
    """
    Split a string of ingredients by the "|" delimiter and strip whitespace.

    Args:
        ingredients (str): A string containing ingredients separated by "|".

    Returns:
        list: A list of individual ingredients.
    """
    return [ingredient.strip() for ingredient in ingredients.split("|") if ingredient.strip()]

def split_instructions(instructions: str) -> list:
    """
    Split a string of instructions by the "|" delimiter and strip whitespace.

    Args:
        instructions (str): A string containing instructions separated by "|".

    Returns:
        list: A list of individual instructions.
    """
    return [step.strip() for step in instructions.split("|") if step.strip()]