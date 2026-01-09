"""
format module
=============
Package: `src`

Module to format and combine data from different sources

Functions
---------
- `formatData`
"""

from . import models


def formatData(
        games: list[models.Game],
        notes: list[models.Note],
        editors: list[models.Editor],
        /
        ) -> list[models.Data]:
    """
    Combine games, notes and editor data into unified Data objects
    
    Parameters
    ----------
    games : list[models.Game]
        List of games from Steam API
    notes : list[models.Note]
        List of ratings from RAWG API
    editors : list[models.Editor]
        List of publishers from Yahoo Finance API
    
    Returns
    -------
    list[models.Data]
        List of combined data objects
    """
    data_list: list[models.Data] = []

    for game in games:
        # Find matching note by game name
        matching_note = None
        for note in notes:
            if (note.name.lower() == game.name.lower() or 
                note.name_original.lower() == game.name.lower() or
                game.name.lower() in [n.lower() for n in note.alternative_names]):
                matching_note = note
                break

        # Find matching editor by publisher name
        matching_editor = None
        if game.publisher:
            for editor in editors:
                publisher_lower = game.publisher.lower()
                if (publisher_lower in editor.display_name.lower() or
                    publisher_lower in editor.short_name.lower() or
                    publisher_lower in editor.long_name.lower()):
                    matching_editor = editor
                    break

        # Create combined Data object
        data_list.append(models.Data(
            game=game,
            note=matching_note,
            editor=matching_editor
        ))

    return data_list
