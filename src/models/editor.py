"""
editor module
===========
Package: `models`

Module to/that # TODO: set docstring

Classes
-------
- `Editor`
"""


import typing
import datetime


class Editor:
    """
    Editor class
    ==========
    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            display_name: str = "",
            history: dict[datetime.date, float] = {}
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        # Editor info
        self.symbol: str = ""
        self.display_name: str = display_name
        self.short_name: str = ""
        self.long_name: str = ""
        self.country: str = ""
        self.zip: str = ""
        self.city: str = ""
        self.industry: str = ""
        self.sector: str = ""
        self.full_time_employees: int = 0
        self.market_capitalization: int = 0
        self.enterprise_value: int = 0

        # Share info
        self.market: str = ""
        self.currency: str = ""
        self.quote_source_name: str = ""

        # Editor's shares history (day -> share price in currency)
        self.history: dict[datetime.date, float] = history
