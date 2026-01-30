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


from . import utils, models, api, format  # type: ignore # noqa: F401


def getData(
        *,
        publishers_ids: list[models.PublisherId],
        steam_max_games_per_publisher: int | None = None,
        rawg_key: str,
        min_score_similarity: float,
        ) -> list[models.Data]:
    """
    Retrieves and formats data from various APIs.

    Parameters:
        publishers_ids (list[models.PublisherId]): List of publisher identities to fetch
        steam_max_games_per_publisher (int | None): Maximum number of games per publisher to fetch from Steam API (None for all)
        rawg_key (str): API key for RAWG API
        min_score_similarity (float): Minimum score for name similarity acceptance (0.0 - 1.0)

    Returns:
        out (list[models.Data]): Formatted data from Steam, RAWG, and yfinance APIs
    """
    utils.echoInfo("\n--- Démarrage de la récupération des données ---\n", indent=0)

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
        min_score_similarity=min_score_similarity,
    )

    utils.echoInfo("\n--- Récupération des données terminée ---\n", indent=0)

    return data
