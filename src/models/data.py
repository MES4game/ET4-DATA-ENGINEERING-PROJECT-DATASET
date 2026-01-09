"""
data module
===========
Package: `models`

Module to represent combined game data from multiple sources

Classes
-------
- `Data`
"""


import typing
from datetime import datetime
from .game import Game
from .note import Note
from .editor import Editor


class Data:
    """
    Data class
    ==========
    Class to combine game, rating and publisher information
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            game: Game,
            note: Note | None = None,
            editor: Editor | None = None
            ) -> None:
        """
        Initialize Data with game information and optional ratings/editor data
        """
        self.game: Game = game
        self.note: Note | None = note
        self.editor: Editor | None = editor

    def _get_stock_data_around_release(self) -> dict:
        """Calculate stock data before, at, and after game release"""
        if not self.editor or not self.editor.history:
            return {}
        
        release_date = self.game.release_date
        dates = sorted(self.editor.history.keys())
        
        # Find closest dates
        before_date = None
        at_date = None
        after_date = None
        
        for date in dates:
            if date < release_date:
                before_date = date
            elif date >= release_date and at_date is None:
                at_date = date
            elif at_date and date > at_date and after_date is None:
                after_date = date
                break
        
        result = {}
        
        if before_date:
            result["stock_price_before_release"] = self.editor.history[before_date]
        if at_date:
            result["stock_price_at_release"] = self.editor.history[at_date]
        if after_date:
            result["stock_price_after_release"] = self.editor.history[after_date]
        
        # Calculate variations
        if before_date and after_date:
            price_before = self.editor.history[before_date]
            price_after = self.editor.history[after_date]
            if price_before > 0:
                result["price_variation_percent"] = ((price_after - price_before) / price_before) * 100
        
        return result

    def to_dict(self: typing.Self) -> dict:
        """Convert Data object to dictionary matching the schema"""
        current_time = datetime.now().isoformat()
        
        # Base game data
        data_dict = {
            "name": self.game.name,
            "price": self.game.price,
            "required_age": self.game.required_age,
            "for_windows": self.game.for_windows,
            "for_linux": self.game.for_linux,
            "for_mac": self.game.for_mac,
            "release_date": self.game.release_date.isoformat(),
            "genres": ", ".join(self.game.genres) if self.game.genres else None,
            "publisher": self.game.publisher,
            "data_source": "Steam",
            "last_updated": current_time,
            "ingestion_date": current_time
        }

        # Add rating data if available
        if self.note:
            data_dict.update({
                "name_original": self.note.name_original,
                "alternative_names": self.note.alternative_names,
                "metacritic": self.note.metacritic,
                "rating": self.note.rating,
                "ratings_count": self.note.ratings_count
            })
            data_dict["data_source"] += "|RAWG"

        # Add editor/stock data if available
        if self.editor:
            data_dict.update({
                "ticker_symbol": self.editor.symbol,
                "stock_exchange": self.editor.market,
                "currency": self.editor.currency,
                "is_public": True
            })
            data_dict["data_source"] += "|Yahoo"
            
            # Add stock price data around release
            stock_data = self._get_stock_data_around_release()
            data_dict.update(stock_data)
            
            # Add most recent stock data
            if self.editor.history:
                latest_date = max(self.editor.history.keys())
                data_dict.update({
                    "date": latest_date.isoformat(),
                    "close_price": self.editor.history[latest_date],
                    "adjusted_close": self.editor.history[latest_date]
                })
        else:
            data_dict["is_public"] = False

        return data_dict
