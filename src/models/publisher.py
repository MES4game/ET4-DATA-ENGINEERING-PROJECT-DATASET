"""
publisher module
================
Package: `models`

Module to define a video game publisher and stock information.

Classes
-------
- `PublisherId`
- `StockValue`
- `Publisher`
"""


import typing
import datetime


class PublisherId:
    """
    PublisherId class
    =================
    Defines a tracked game publisher identities.

    Attributes:
        name (str) : Publisher name
        symbol (str) : Stock symbol
        steam_names (list[str]) : List of publisher's name variations on Steam
        rawg_name (str) : Publisher's name variation on RAWG
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            name: str,
            symbol: str,
            steam_names: list[str],
            rawg_name: str,
            ) -> None:
        """
        Initializes a PublisherId instance.

        Parameters:
            name (str) : Publisher name
            symbol (str) : Stock symbol on Yahoo Finance
            steam_names (list[str]) : List of publisher's name variations on Steam
            rawg_name (str) : Publisher's name variations on RAWG
        """
        self.name: str = name
        self.symbol: str = symbol
        self.steam_names: list[str] = steam_names
        self.rawg_name: str = rawg_name


class StockValue:
    """
    StockValue class
    ================
    Defines stock value information for a specific date.

    Attributes:
        close_price (float): Closing price of the stock
        volume (int): Trading volume of the stock
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            close_price: float,
            volume: int,
            ) -> None:
        """
        Initialize StockValue with closing price and volume.

        Parameters:
            close_price (float): Closing price of the stock
            volume (int): Trading volume of the stock
        """
        self.close_price: float = close_price
        self.volume: int = volume


class Publisher:
    """
    Publisher class
    ==========
    Defines a video game publisher and stock information.

    Attributes:
        used_name (str): Name used to find the publisher
        symbol (str): Stock symbol of the publisher
        short_name (str): Short name of the publisher
        long_name (str): Long name of the publisher
        currency (str): Currency of the stock prices
        history (dict[datetime.date, StockValue]): Historical stock data
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            used_name: str,
            symbol: str,
            short_name: str,
            long_name: str,
            currency: str,
            history: dict[datetime.date, StockValue],
            ) -> None:
        """
        Initialize Publisher with stock and company information.

        Parameters:
            used_name (str): Name used to find the publisher
            symbol (str): Stock symbol of the publisher
            short_name (str): Short name of the publisher
            long_name (str): Long name of the publisher
            currency (str): Currency of the stock prices
            history (dict[datetime.date, StockValue]): Historical stock data
        """
        self.used_name: str = used_name
        self.symbol: str = symbol
        self.short_name: str = short_name
        self.long_name: str = long_name
        self.currency: str = currency
        self.history: dict[datetime.date, StockValue] = history
