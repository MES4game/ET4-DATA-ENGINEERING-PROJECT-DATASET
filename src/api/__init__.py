"""
api package
===========

Package to/that # TODO: set docstring

Functions
---------
- `getGames`
- `getNotes`
- `getEditors`
- `getStocks`
"""


from .. import models  # type: ignore # noqa: F401
from .steam import getGames  # type: ignore # noqa: F401
from .rawg import getNotes  # type: ignore # noqa: F401
from .yfinance import getEditors, getStocks  # type: ignore # noqa: F401
