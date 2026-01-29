"""
game module
===========
Package: `models`

Module to define a video game.

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
    Defines a video game.

    Attributes:
        name (str): Name of the game
        price (int): Price of the game in currency cents (e.g., 1999 = 19.99 currency)
        currency (str): Currency code (e.g., "USD")
        publisher (str): Publisher of the game
        for_windows (bool): Whether the game is available for Windows
        for_mac (bool): Whether the game is available for Mac
        for_linux (bool): Whether the game is available for Linux
        genres (list[str]): Genres of the game
        release_date (datetime.date): Release date of the game
        data_source (str): Source URL of the game data
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            name: str,
            price: int,
            currency: str,
            publisher: str,
            for_windows: bool,
            for_mac: bool,
            for_linux: bool,
            genres: list[str],
            release_date: datetime.date,
            data_source: str,
            ) -> None:
        """
        Initializes a Game instance.

        Parameters:
            name (str): Name of the game
            price (int): Price of the game in currency cents (e.g., 1999 = 19.99 currency)
            currency (str): Currency code (e.g., "USD")
            publisher (str): Publisher of the game
            for_windows (bool): Whether the game is available for Windows
            for_mac (bool): Whether the game is available for Mac
            for_linux (bool): Whether the game is available for Linux
            genres (list[str]): Genres of the game
            release_date (datetime.date): Release date of the game
            data_source (str): Source URL of the game data
        """
        self.name: str = name
        self.price: int = price
        self.currency: str = currency
        self.publisher: str = publisher
        self.for_windows: bool = for_windows
        self.for_mac: bool = for_mac
        self.for_linux: bool = for_linux
        self.genres: list[str] = genres
        self.release_date: datetime.date = release_date
        self.data_source: str = data_source
