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
from . import utils, models


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

    utils.echoInfo(f"--- Début de l'extraction RAWG.io pour {len(publishers_ids)} éditeurs ---", indent=1)

    for publisher in publishers_ids:
        utils.echoInfo(f"Récupération des notes pour \"{publisher.name}\"...", indent=2)

        old_length: int = len(note_list)

        i: int = 1
        while True:
            try:
                time.sleep(0.5)  # Respect API rate limits

                r_notes = requests.get(notes_url, params=notes_params | {"page": i, "publishers": publisher.rawg_name})
                r_notes.raise_for_status()
                data: dict[str, typing.Any] = r_notes.json()
                matches: list[dict[str, typing.Any]] = data.get("results", [])

                utils.echoInfo(f"Page {i}: {len(matches)} résultats", indent=3)

                if len(matches) == 0:
                    break

                for match in matches:
                    name: str | None = utils.extractValueFromDict(match, 'name', None, str)
                    slug: str | None = utils.extractValueFromDict(match, 'slug', None, str)
                    release_date: datetime.date | None = utils.extractValueFromDict(match, 'released', None, datetime.date)
                    tba: bool | None = utils.extractValueFromDict(match, 'tba', None, bool)
                    metacritic: int | None = utils.extractValueFromDict(match, 'metacritic', None, int)
                    rating: float | None = utils.extractValueFromDict(match, 'rating', None, float)
                    ratings_count: int | None = utils.extractValueFromDict(match, 'ratings_count', None, int)
                    suggestions_count: int | None = utils.extractValueFromDict(match, 'suggestions_count', None, int)
                    reviews_count: int | None = utils.extractValueFromDict(match, 'reviews_count', None, int)

                    note_list.append(models.Note(
                        publisher=publisher.name,
                        name=name,
                        slug=slug,
                        release_date=release_date,
                        tba=tba,
                        metacritic=metacritic,
                        rating=rating,
                        ratings_count=ratings_count,
                        suggestions_count=suggestions_count,
                        reviews_count=reviews_count,
                        data_source=r_notes.url,
                    ))

                if re.search(r'{\s*"count"\s*:\s*\d+\s*,\s*"next"\s*:\s*null\s*,\s*"previous"\s*:\s*"?[^"]*"?\s*,\s*"results"\s*:\s*', r_notes.text) is not None:
                    break

                i += 1

            except Exception as e:
                utils.echoError(f"Page {i}: {e}", indent=3)
                break

        utils.echoInfo(f"Total des notes trouvés pour \"{publisher.name}\": {len(note_list) - old_length}", indent=2)

    utils.echoInfo("--- Fin de la récupération des notes sur RAWG.io ---", indent=1)

    return note_list
