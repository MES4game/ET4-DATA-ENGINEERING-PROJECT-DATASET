"""
src package
===========

Package containing core modules and functionalities.

Sub-packages
------------
- `models`
- `api`
Modules
-------
- `echo`
- `format`
Functions
---------
- `getData`
"""


from . import echo, models, api, format  # type: ignore # noqa: F401


def getData(
        *,
        publishers_ids: list[models.PublisherId],
        steam_max_games_per_publisher: int | None = None,
        rawg_key: str,
        ) -> list[models.Data]:
    """
    Retrieves and formats data from various APIs.

    Parameters:
        publishers_ids (list[models.PublisherId]): List of publisher identities to fetch
        steam_max_games_per_publisher (int | None): Maximum number of games per publisher to fetch from Steam API (None for all)

    Returns:
        out (list[models.Data]): Formatted data from Steam, RAWG, and yfinance APIs
    """
    echo.echoInfo("\n--- Démarrage de la récupération des données ---\n", indent=0)

    data: list[models.Data] = format.formatData(
        games=api.getGames(
            publishers_ids=publishers_ids,
            max_games_per_publisher=steam_max_games_per_publisher,
        ),
        notes=api.getNotes(
            publishers_ids=publishers_ids,
            key=rawg_key,
        ),
        publishers=api.getPublishers(publishers_ids=publishers_ids),
    )

    echo.echoInfo("\n--- Récupération des données terminée ---\n", indent=0)

    return data
