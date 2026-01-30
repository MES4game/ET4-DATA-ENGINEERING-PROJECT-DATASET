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
        publisher (str | None): Name of the publisher
        name (str | None): Name of the game
        slug (str | None): Slug identifier of the game
        release_date (datetime.date | None): Release date of the game
        tba (bool | None): Whether the release date is to be announced
        metacritic (int | None): Metacritic score (0-100)
        rating (float | None): User rating (0.0-5.0)
        ratings_count (int | None): Number of user ratings
        suggestions_count (int | None): Number of user suggestions
        reviews_count (int | None): Number of user reviews
        data_source (str): Source URL of the note data
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            publisher: str | None,
            name: str | None,
            slug: str | None,
            release_date: datetime.date | None,
            tba: bool | None,
            metacritic: int | None,
            rating: float | None,
            ratings_count: int | None,
            suggestions_count: int | None,
            reviews_count: int | None,
            data_source: str,
            ) -> None:
        """
        Initializes a Note instance.

        Parameters:
            publisher (str | None): Name of the publisher
            name (str | None): Name of the game
            slug (str | None): Slug identifier of the game
            release_date (datetime.date | None): Release date of the game
            tba (bool | None): Whether the release date is to be announced
            metacritic (int | None): Metacritic score (0-100)
            rating (float | None): User rating (0.0-5.0)
            ratings_count (int | None): Number of user ratings
            suggestions_count (int | None): Number of user suggestions
            reviews_count (int | None): Number of user reviews
            data_source (str): Source URL of the note data
        """
        self.publisher: str | None = publisher
        self.name: str | None = name
        self.slug: str | None = slug
        self.release_date: datetime.date | None = release_date
        self.tba: bool | None = tba
        self.metacritic: int | None = metacritic
        self.rating: float | None = rating
        self.ratings_count: int | None = ratings_count
        self.suggestions_count: int | None = suggestions_count
        self.reviews_count: int | None = reviews_count
        self.data_source: str = data_source
