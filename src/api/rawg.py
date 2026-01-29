"""
rawg API module
===============
Package: `api`

Retrieves game notes from RAWG API based on given publishers.

Functions
---------
- `getNotes`
"""


import typing
import time
import datetime
import re
import requests
from . import echo, models


def getNotes(
        *,
        publishers_ids: list[models.PublisherId],
        key: str,
        ) -> list[models.Note]:
    """
    Retrieves a list of game notes specifically for given publishers.

    Parameters:
        publishers_ids (list[models.PublisherId]): List of publisher identities to fetch
        key (str): RAWG API key

    Returns:
        out (list[models.Note]): List of retrieved notes
    """
    note_list: list[models.Note] = []

    # URL et paramètres pour les notes des jeux
    notes_url = "https://api.rawg.io/api/games"
    notes_params: dict[str, str | int] = {
        "key": key,
        "page_size": 100,
        "ordering": "released",
        "platforms": "4,5,6",
        "stores": "1",
        "publishers": ",".join(map(lambda x: x.rawg_name, publishers_ids)),
    }

    echo.echoInfo(f"--- Début de l'extraction RAWG.io pour {len(publishers_ids)} éditeurs ---", indent=1)

    for publisher in publishers_ids:
        echo.echoInfo(f"Récupération des notes pour \"{publisher.name}\"...", indent=2)

        old_length: int = len(note_list)

        i: int = 1
        while True:
            try:
                time.sleep(0.5)  # Respect API rate limits

                r_notes = requests.get(notes_url, params=notes_params | {"page": i, "publishers": publisher.rawg_name})
                r_notes.raise_for_status()
                data: dict[str, typing.Any] = r_notes.json()
                matches: list[dict[str, typing.Any]] = data.get("results", [])

                echo.echoInfo(f"Page {i}: {len(matches)} résultats", indent=3)

                if len(matches) == 0:
                    break

                for match in matches:
                    note_list.append(models.Note(
                        name=str(match.get('name', '') or ''),
                        publisher=publisher.name,
                        release_date=datetime.datetime.strptime(str(match.get('released', '1970-01-01') or '1970-01-01'), "%Y-%m-%d").date(),
                        metacritic=int(match.get('metacritic', 0) or 0),
                        rating=float(match.get('rating', 0.0) or 0.0),
                        ratings_count=int(match.get('ratings_count', 0) or 0),
                        data_source=r_notes.url,
                    ))

                if re.search(r'{\s*"count"\s*:\s*\d+\s*,\s*"next"\s*:\s*null\s*,\s*"previous"\s*:\s*"?[^"]*"?\s*,\s*"results"\s*:\s*', r_notes.text) is not None:
                    break

                i += 1

            except Exception as e:
                echo.echoError(f"Page {i}: {e}", indent=3)
                break

        echo.echoInfo(f"Total des notes trouvés pour \"{publisher.name}\": {len(note_list) - old_length}", indent=2)

    echo.echoInfo("--- Fin de la récupération des notes sur RAWG.io ---", indent=1)

    return note_list
