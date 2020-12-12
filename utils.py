"""
Tools
"""

def is_valid_list_list_float(list_list_float) -> bool:
    """
    Return True if list_list_float verifies:
        - not None
        - list type
        - float type for all values

    :return: bool
    """
    return (
            list_list_float is not None
            and isinstance(list_list_float, list)
            and all
                (
                [
                    isinstance(x, float)
                    for sublist in list_list_float
                    for x in sublist
                ]
            )
    )
