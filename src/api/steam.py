"""
steam API module
================
Package: `api`

Retrieves game details from Steam Store API based on given publishers.

Functions
---------
- `getGames`
"""


import typing
import requests
import time
import datetime
import re
from . import echo, models


def getGames(
        *,
        publishers_ids: list[models.PublisherId],
        max_games_per_publisher: int | None = None,
        ) -> list[models.Game]:
    """
    Retrieves a list of games specifically for given publishers.

    Parameters:
        publishers_ids (list[models.PublisherId]): List of publisher identities to fetch
        max_games_per_publisher (int | None): Maximum number of games per publisher to fetch (None for all)

    Returns:
        out (list[models.Game]): List of retrieved games
    """
    game_list: list[models.Game] = []

    # URL et paramètres pour la recherche des jeux par editeur
    search_url = "https://store.steampowered.com/search/results/"
    search_params = {
        "category1": 998,
        "json": 1,
        "count": 100
    }
    # URL et paramètres pour les détails des jeux
    details_url = "https://store.steampowered.com/api/appdetails"
    details_params = {
        "filters": "price_overview,platforms,genres,release_date",
        "l": "english",
    }

    echo.echoInfo(f"--- Début de l'extraction Steam pour {len(publishers_ids)} éditeurs ---", indent=1)

    for publisher in publishers_ids:

        # 1. Recherche des ids de jeux pour l'éditeur
        echo.echoInfo(f"Recherche des jeux pour : \"{publisher.name}\"...", indent=2)

        game_id_name_map: dict[int, str] = {}

        for publisher_steam_name in publisher.steam_names:
            echo.echoInfo(f"Recherche pour le nom : \"{publisher_steam_name}\"", indent=3)

            i: int = 0
            while True:
                try:
                    time.sleep(0.5)  # Respect API rate limits

                    r_search = requests.get(search_url, params=search_params | {"start": search_params.get("count", 50) * i, "publisher": publisher_steam_name})
                    r_search.raise_for_status()

                    matches = re.findall(r'"name":\s*"([^"]*)",\s*"logo":\s*"https:\\/\\/shared.fastly.steamstatic.com\\/store_item_assets\\/steam\\/apps\\/(\d+)\\/[^"]+', r_search.text)
                    echo.echoInfo(f"Page {i + 1}: {len(matches)} résultats", indent=4)

                    if len(matches) == 0:
                        break

                    for name, id in matches:
                        if game_id_name_map.get(int(id)) is None:
                            game_id_name_map[int(id)] = name

                    if max_games_per_publisher and len(game_id_name_map) >= max_games_per_publisher:
                        echo.echoInfo(f"Limite de {max_games_per_publisher} jeux atteinte pour l'éditeur \"{publisher.name}\".", indent=4)
                        break

                    i += 1

                except Exception as e:
                    echo.echoError(f"Page {i + 1}: {e}", indent=4)
                    break

        echo.echoInfo(f"Total des jeux trouvés pour \"{publisher.name}\": {len(game_id_name_map)}", indent=2)

        # 2. Récupération des détails pour chaque jeu
        echo.echoInfo(f"Récupération des détails des jeux de \"{publisher.name}\"...", indent=2)
        echo.echoInfo("N'oubliez pas que pour chaque jeu il faut compter un délai (1.5s) pour respecter les limites de l'API Steam.", indent=3)

        for id, name in list(game_id_name_map.items())[:max_games_per_publisher]:
            echo.echoInfo(f"Récupération des détails pour le jeu \"{name}\"...", indent=3)

            try:
                time.sleep(1.5)  # Respect API rate limits

                r_details: requests.Response = requests.get(details_url, params=details_params | {"appids": id})
                r_details.raise_for_status()
                data: dict[str, typing.Any] = r_details.json()

                if data.get(str(id), {}).get('success', False):
                    game_data: dict[str, typing.Any] = data.get(str(id), {}).get('data', {}) or {}

                    price_overview: dict[str, typing.Any] = game_data.get('price_overview', {}) or {}
                    platforms: dict[str, typing.Any] = game_data.get('platforms', {}) or {}
                    genres: list[dict[str, typing.Any]] = game_data.get('genres', []) or []
                    release_date: dict[str, typing.Any] = game_data.get('release_date', {}) or {}

                    game_list.append(models.Game(
                        name=name,
                        price=int(price_overview.get('initial', 0) or 0),
                        currency=str(price_overview.get('currency', 'USD') or 'USD'),
                        publisher=publisher.name,
                        for_windows=bool(platforms.get('windows', False) or False),
                        for_mac=bool(platforms.get('mac', False) or False),
                        for_linux=bool(platforms.get('linux', False) or False),
                        genres=list(map(lambda x: str(x.get('description', '')), genres) or []),
                        release_date=datetime.datetime.strptime(str(release_date.get('date', '1970-01-01') or '1970-01-01'), "%d %b, %Y").date(),
                        data_source=r_details.url,
                    ))
                else:
                    echo.echoError(f"Échec de la récupération des détails pour le jeu \"{name}\".", indent=3)

            except Exception as e:
                echo.echoError(f"Erreur lors de la récupération des détails pour le jeu \"{name}\": {e}", indent=3)

    echo.echoInfo("--- Fin de la récupération des jeux sur Steam ---", indent=1)

    return game_list
