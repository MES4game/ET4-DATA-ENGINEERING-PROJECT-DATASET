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
        used_name (str | None): Name used to find the publisher
        symbol (str | None): Stock symbol of the publisher
        short_name (str | None): Short name of the publisher
        long_name (str | None): Long name of the publisher
        currency (str | None): Currency of the stock prices
        history (dict[datetime.date, StockValue]): Historical stock data
        market (str | None): Market where the publisher stocks are traded
        country (str | None): Country of the publisher
        fullTimeEmployees (int | None): Number of full-time employees
        all_time_high (float | None): All-time high stock price
        all_time_low (float | None): All-time low stock price
        total_cash (int | None): Total cash of the publisher
        total_debt (int | None): Total debt of the publisher
        total_revenue (int | None): Total revenue of the publisher
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            used_name: str | None,
            symbol: str | None,
            short_name: str | None,
            long_name: str | None,
            currency: str | None,
            history: dict[datetime.date, StockValue],
            market: str | None,
            country: str | None,
            fullTimeEmployees: int | None,
            all_time_high: float | None,
            all_time_low: float | None,
            total_cash: int | None,
            total_debt: int | None,
            total_revenue: int | None,
            ) -> None:
        """
        Initialize Publisher with stock and company information.

        Parameters:
            used_name (str | None): Name used to find the publisher
            symbol (str | None): Stock symbol of the publisher
            short_name (str | None): Short name of the publisher
            long_name (str | None): Long name of the publisher
            currency (str | None): Currency of the stock prices
            history (dict[datetime.date, StockValue]): Historical stock data
            market (str | None): Market where the publisher stocks are traded
            country (str | None): Country of the publisher
            fullTimeEmployees (int | None): Number of full-time employees
            all_time_high (float | None): All-time high stock price
            all_time_low (float | None): All-time low stock price
            total_cash (int | None): Total cash of the publisher
            total_debt (int | None): Total debt of the publisher
            total_revenue (int | None): Total revenue of the publisher
        """
        self.used_name: str | None = used_name
        self.symbol: str | None = symbol
        self.short_name: str | None = short_name
        self.long_name: str | None = long_name
        self.currency: str | None = currency
        self.history: dict[datetime.date, StockValue] = history
        self.market: str | None = market
        self.country: str | None = country
        self.fullTimeEmployees: int | None = fullTimeEmployees
        self.all_time_high: float | None = all_time_high
        self.all_time_low: float | None = all_time_low
        self.total_cash: int | None = total_cash
        self.total_debt: int | None = total_debt
        self.total_revenue: int | None = total_revenue
