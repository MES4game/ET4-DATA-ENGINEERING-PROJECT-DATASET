"""
format module
=============
Package: `src`

Module to format and combine data from different sources.

Functions
---------
- `formatData`
"""

import functools
import re
import difflib
from . import models


@functools.cache
def __sanitizePublisherName(name: str) -> str:
    """
    Sanitize publisher name for matching across different data sources.

    Parameters:
        name (str): Original publisher name

    Returns:
        out (str): Sanitized publisher name
    """
    name = name.lower()

    name = re.sub(r"\(.*?\)", "", name)
    name = name.replace("&", "and")
    name = re.sub(r"[^a-z0-9\s]", "", name)

    words = ["inc", "ltd", "llc", "co", "corporation", "corp", "company", "com", "organisation", "org", "group", "holdings", "holding", "hldgs", "entertainment", "entertain", "plc", "gmbh", "sa", "ag", "ab", "shs", "ord", "oyj"]
    name = re.sub(r"\b(" + "|".join(words) + r")\b", "", name)

    name = name.strip()
    name = re.sub(r"\s+", " ", name)

    return name


@functools.cache
def __matchPublisherName(name: str, publisher: models.Publisher) -> bool:
    """
    Match a publisher name against a list of candidate names.

    Parameters:
        name (str): Publisher name to match
        publisher (models.Publisher): Publisher object containing candidate names

    Returns:
        out (bool): True if a match is found, False otherwise
    """
    sanitized_name = __sanitizePublisherName(name)

    if difflib.SequenceMatcher(None, publisher.long_name, sanitized_name).ratio() > 0.9:
        return True

    if difflib.SequenceMatcher(None, publisher.short_name, sanitized_name).ratio() > 0.9:
        return True

    # Check with our own defined name (should always match if data is correct, just a fallback)
    if __sanitizePublisherName(publisher.used_name) == sanitized_name:
        return True

    return False


@functools.cache
def __normalizeGameName(name: str) -> str:
    """
    Normalize game name for comparison.

    Parameters:
        name (str): Original game name

    Returns:
        out (str): Normalized game name
    """
    name = name.lower()

    name = name.replace("&", "and")
    name = re.sub(r"[^a-z0-9\s]", " ", name)

    name = name.strip()
    name = re.sub(r"\s+", " ", name)

    return name


def __calculateMatchScore(game: models.Game, note: models.Note) -> float:
    """
    Calculate a similarity score between a game and a note based on name and release date.

    Parameters:
        game (models.Game): Game object
        note (models.Note): Note object

    Returns:
        out (float): Similarity score between -0.5 and 1.3 (higher is better) (0.0 to 1.0 for name similarity plus -0.5 to 0.3 for date bonus/penalty)
    """
    bonus_score: float = 0.0

    # 1. Release Date Heuristic (Bonus/Penalty)
    date_diff: int = abs((game.release_date - note.release_date).days)

    if date_diff <= 7:
        bonus_score = 0.3
    if date_diff <= 30:
        bonus_score = 0.25
    elif date_diff <= 90:
        bonus_score = 0.15
    elif date_diff <= 180:
        bonus_score = 0.1
    elif date_diff <= 365:
        bonus_score = -0.1
    elif date_diff <= 365 * 2:
        bonus_score = -0.3
    else:
        bonus_score = -0.5

    # 2. Name Similarity (Base Score)
    norm_game: str = __normalizeGameName(game.name)
    norm_note: str = __normalizeGameName(note.name)

    if norm_game == norm_note:
        return 1.0 + bonus_score

    base_score = difflib.SequenceMatcher(None, norm_game, norm_note).ratio()

    return base_score + bonus_score


def formatData(
        *,
        games: list[models.Game],
        notes: list[models.Note],
        publishers: list[models.Publisher],
        ) -> list[models.Data]:
    """
    Combine games, notes and publisher data into unified Data objects.

    Parameters:
        games (list[models.Game]) : List of games from Steam API
        notes (list[models.Note]) : List of ratings from RAWG API
        publisher (list[models.Publisher]) : List of publishers from Yahoo Finance API

    Returns:
        out (list[models.Data]): List of combined data objects
    """
    data: list[models.Data] = []

    for publisher in publishers:

        # Find all games and notes for this publisher
        filtered_games = [game for game in games if __matchPublisherName(game.publisher, publisher)]
        filtered_notes = [note for note in notes if __matchPublisherName(note.publisher, publisher)]

        for game in filtered_games:

            # Iterate through all filtered notes to find the best candidate
            best_match: models.Note | None = None
            highest_score: float = 0.0

            for note in filtered_notes:
                score = __calculateMatchScore(game, note)

                if score > highest_score:
                    highest_score = score
                    best_match = note

            # Create combined Data object
            data.append(models.Data(
                game=game,
                note=best_match if highest_score >= 0.85 else None,
                publisher=publisher
            ))

    return data
