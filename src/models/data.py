"""
data module
===========
Package: `models`

Module to represent combined game data from multiple sources.

Classes
-------
- `Data`
"""


import typing
import datetime
from . import Game, Note, Publisher


class Data:
    """
    Data class
    ==========
    Class to combine game, rating and publisher information

    Attributes:
        game (Game): Game information
        note (Note | None): Optional game rating information
        publisher (Publisher | None): Optional publisher information

    Methods
    -------
    - `toDict`: Convert Data object to dictionary matching the schema
    - `__getNearestDateWithStockData`: Find the nearest date with stock data
    - `__getStockDataAtDate`: Retrieve stock data for a specific date
    - `__getStockData`: Calculate stock data before, at, and after game release
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            game: Game,
            publisher: Publisher,
            note: Note | None,
            ) -> None:
        """
        Initialize Data with game information, publisher data and optional ratings data.

        Parameters:
            game (Game): Game information
            publisher (Publisher): Publisher information
            note (Note | None): Optional game rating information
        """
        self.game: Game = game
        self.note: Note | None = note
        self.publisher: Publisher = publisher

    def __getNearestDateWithStockData(
            self: typing.Self,
            /,
            *,
            target: datetime.date,
            before: bool,
            ) -> datetime.date | None:
        """
        Find the nearest date with stock data.

        Parameters:
            target (datetime.date): Reference date to find nearest stock data
            before (bool): If True, search for the nearest date before the reference date; otherwise, search after

        Returns:
            out (datetime.date | None): Nearest date with stock data or None if not found
        """
        nearest_date: datetime.date | None = None

        for d in self.publisher.history.keys():
            if (before and d > target) or (not before and d < target):
                continue
            if nearest_date is None or abs(d - target) < abs(nearest_date - target):
                nearest_date = d

        return nearest_date

    def __getStockDataAtDate(
            self: typing.Self,
            /,
            *,
            target_date: datetime.date,
            release_date: datetime.date,
            ) -> dict[str, typing.Any]:
        """
        Retrieve stock data for a specific date.

        Parameters:
            target_date (datetime.date): Target date to find stock data for
            release_date (datetime.date): Nearest date from game release with stock data

        Returns:
            out (dict[str, typing.Any]): Stock data for the date
        """
        target_stock_value = self.publisher.history[target_date]
        release_stock_value = self.publisher.history[release_date]

        return {
            "date": target_date.isoformat(),
            "currency": self.publisher.currency,
            "close_price": target_stock_value.close_price,
            "volume": target_stock_value.volume,
            "price_variation_percentage": round((target_stock_value.close_price - release_stock_value.close_price) * 100 / release_stock_value.close_price, 2),
            "volume_variation_percentage": round((target_stock_value.volume - release_stock_value.volume) * 100 / release_stock_value.volume, 2),
            "data_source": "yfinance python package (https://finance.yahoo.com/)",
        }

    def __getStockData(self: typing.Self, /) -> dict[str, typing.Any]:
        """
        Calculate stock data before, at, and after game release.

        Returns:
            out (dict[str, typing.Any]): Stock infos and price values
        """
        result: dict[str, typing.Any] = {
            "publisher": self.publisher.long_name,
            "ticker": self.publisher.symbol,
            "data_source": "yfinance python package (https://finance.yahoo.com/)",
        }

        # Find closest dates with stock data
        at_release: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date, before=True)

        if at_release is None:
            return result | {
                "at_release": None,
                "month_before": None,
                "week_before": None,
                "day_before": None,
                "day_after": None,
                "week_after": None,
                "month_after": None,
            }

        month_before: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date - datetime.timedelta(days=30), before=True)
        week_before: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date - datetime.timedelta(days=7), before=True)
        day_before: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date - datetime.timedelta(days=1), before=True)
        day_after: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date + datetime.timedelta(days=1), before=False)
        week_after: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date + datetime.timedelta(days=7), before=False)
        month_after: datetime.date | None = self.__getNearestDateWithStockData(target=self.game.release_date + datetime.timedelta(days=30), before=False)

        result["at_release"] = self.__getStockDataAtDate(target_date=at_release, release_date=at_release)

        if month_before:
            result["month_before"] = self.__getStockDataAtDate(target_date=month_before, release_date=at_release)
        else:
            result["month_before"] = None

        if week_before:
            result["week_before"] = self.__getStockDataAtDate(target_date=week_before, release_date=at_release)
        else:
            result["week_before"] = None

        if day_before:
            result["day_before"] = self.__getStockDataAtDate(target_date=day_before, release_date=at_release)
        else:
            result["day_before"] = None

        if day_after:
            result["day_after"] = self.__getStockDataAtDate(target_date=day_after, release_date=at_release)
        else:
            result["day_after"] = None

        if week_after:
            result["week_after"] = self.__getStockDataAtDate(target_date=week_after, release_date=at_release)
        else:
            result["week_after"] = None

        if month_after:
            result["month_after"] = self.__getStockDataAtDate(target_date=month_after, release_date=at_release)
        else:
            result["month_after"] = None

        return result

    def toDict(self: typing.Self, /) -> dict[str, typing.Any]:
        """
        Convert Data object to dictionary matching the schema.

        Returns:
            out (dict[str, typing.Any]): Dictionary representation of the data
        """
        current_time: str = datetime.datetime.now().isoformat()

        data_dict: dict[str, typing.Any] = {
            "name": self.game.name,
            "price": self.game.price,
            "currency": self.game.currency,
            "for_windows": self.game.for_windows,
            "for_linux": self.game.for_linux,
            "for_mac": self.game.for_mac,
            "release_date": self.game.release_date.isoformat(),
            "genres": self.game.genres,
            "metacritic": self.note.metacritic if self.note else None,
            "rating": self.note.rating if self.note else None,
            "ratings_count": self.note.ratings_count if self.note else None,
            "stocks": self.__getStockData(),
            "data_source_game": self.game.data_source,
            "data_source_note": self.note.data_source if self.note else None,
            "last_updated": current_time,
            "ingestion_date": current_time,
        }

        return data_dict
