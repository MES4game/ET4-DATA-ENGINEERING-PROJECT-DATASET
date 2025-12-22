"""
game module
===========
Package: `models`

Module to/that # TODO: set docstring

Classes
-------
- `Game`
"""


import typing
import datetime


class Game:
    """
    Game class
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
            price: int = 0,
            required_age: int = 0,
            publisher: str = "",
            for_windows: bool = False,
            for_mac: bool = False,
            for_linux: bool = False,
            genres: list[str] = [],
            release_date: datetime.date = datetime.date.today()
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        # Name of the game
        self.name: str = name

        # Price of the game in USD cents (e.g., 1999 = $19.99)
        self.price: int = price

        # Required age (in year) to play the game
        self.required_age: int = required_age

        # Publisher of the game
        self.publisher: str = publisher

        # Supported platforms
        self.for_windows: bool = for_windows
        self.for_mac: bool = for_mac
        self.for_linux: bool = for_linux

        # Genres of the game
        self.genres: list[str] = genres

        # Release date of the game
        self.release_date: datetime.date = release_date
