"""
note module
===========
Package: `models`

Module to define a video game note/rating.

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
    Defines a video game note/rating.

    Attributes:
        name (str): Name of the game
        publisher (str): Name of the publisher
        release_date (datetime.date): Release date of the game
        metacritic (int): Metacritic score (0-100)
        rating (float): User rating (0.0-5.0)
        ratings_count (int): Number of user ratings
        data_source (str): Source URL of the note data
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            name: str,
            publisher: str,
            release_date: datetime.date,
            metacritic: int,
            rating: float,
            ratings_count: int,
            data_source: str,
            ) -> None:
        """
        Initializes a Note instance.

        Parameters:
            name (str): Name of the game
            publisher (str): Name of the publisher
            release_date (datetime.date): Release date of the game
            metacritic (int): Metacritic score (0-100)
            rating (float): User rating (0.0-5.0)
            ratings_count (int): Number of user ratings
            data_source (str): Source URL of the note data
        """
        self.name: str = name
        self.publisher: str = publisher
        self.release_date: datetime.date = release_date
        self.metacritic: int = metacritic
        self.rating: float = rating
        self.ratings_count: int = ratings_count
        self.data_source: str = data_source
