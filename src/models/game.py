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
        name (str | None): Name of the game
        price (int | None): Price of the game in currency cents (e.g., 1999 = 19.99 currency)
        currency (str | None): Currency code (e.g., "USD")
        publisher (str | None): Publisher of the game
        for_windows (bool | None): Whether the game is available for Windows
        for_mac (bool | None): Whether the game is available for Mac
        for_linux (bool | None): Whether the game is available for Linux
        genres (list[str] | None): Genres of the game
        release_date (datetime.date | None): Release date of the game
        recommendations_count (int | None): Number of recommendations for the game
        data_source (str): Source URL of the game data
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            name: str | None,
            price: int | None,
            currency: str | None,
            publisher: str | None,
            for_windows: bool | None,
            for_mac: bool | None,
            for_linux: bool | None,
            genres: list[str] | None,
            release_date: datetime.date | None,
            recommendations_count: int | None,
            data_source: str,
            ) -> None:
        """
        Initializes a Game instance.

        Parameters:
            name (str | None): Name of the game
            price (int | None): Price of the game in currency cents (e.g., 1999 = 19.99 currency)
            currency (str | None): Currency code (e.g., "USD")
            publisher (str | None): Publisher of the game
            for_windows (bool | None): Whether the game is available for Windows
            for_mac (bool | None): Whether the game is available for Mac
            for_linux (bool | None): Whether the game is available for Linux
            genres (list[str] | None): Genres of the game
            release_date (datetime.date | None): Release date of the game
            recommendations_count (int | None): Number of recommendations for the game
            data_source (str): Source URL of the game data
        """
        self.name: str | None = name
        self.price: int | None = price
        self.currency: str | None = currency
        self.publisher: str | None = publisher
        self.for_windows: bool | None = for_windows
        self.for_mac: bool | None = for_mac
        self.for_linux: bool | None = for_linux
        self.genres: list[str] | None = genres
        self.release_date: datetime.date | None = release_date
        self.recommendations_count: int | None = recommendations_count
        self.data_source: str = data_source
