"""
note module
===========
Package: `models`

Module to/that # TODO: set docstring

Classes
-------
- `Note`
"""


import typing
import datetime


class Note:
    """
    Note class
    ==========
    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            name: str = "",
            name_original: str = "",
            alternative_names: list[str] = [],
            release_date: datetime.date = datetime.date.today(),
            metacritic: int = 0,
            rating: float = 0.0,
            ratings_count: int = 0
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        # Game info
        self.name: str = name
        self.name_original: str = name_original
        self.alternative_names: list[str] = alternative_names
        self.release_date: datetime.date = release_date

        # Metacritic score (0-100)
        self.metacritic: int = metacritic

        # User rating (0.0-5.0) and number of ratings
        self.rating: float = rating
        self.ratings_count: int = ratings_count
