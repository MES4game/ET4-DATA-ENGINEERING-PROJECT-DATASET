"""
main module
===========

Module to run the data pipeline and export to JSON

Functions
---------
- `main`
"""


import os
import random
import pathlib
import json
import dotenv
import src


dotenv.load_dotenv()


PUBLISHERS: list[src.models.publisher.PublisherId] = [
    src.models.publisher.PublisherId(
        name="Microsoft",
        symbol="MSFT",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Sony",
        symbol="SONY",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Tencent",
        symbol="TCEHY",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="NetEase",
        symbol="NTES",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Electronic Arts",
        symbol="EA",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Take-Two Interactive",
        symbol="TTWO",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Warner Bros. Discovery",
        symbol="WBD",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Ubisoft",
        symbol="UBI.PA",
        steam_names=["Ubisoft"],
        rawg_name="ubisoft-entertainment",
    ),
    src.models.publisher.PublisherId(
        name="Capcom",
        symbol="9697.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Square Enix",
        symbol="9684.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Sega",
        symbol="6460.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Bandai Namco",
        symbol="7832.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Konami",
        symbol="9766.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Nexon",
        symbol="3659.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Embracer",
        symbol="EMBRAC-B.ST",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Paradox Interactive",
        symbol="PDX.ST",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="CDProjekt",
        symbol="CDR.WA",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Koei Tecmo",
        symbol="3635.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Krafton",
        symbol="259960.KS",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="NCSoft",
        symbol="036570.KS",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Kadokawa",
        symbol="9468.T",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Bilibili",
        symbol="BILI",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Digital Bros",
        symbol="DIB.MI",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Devolver Digital",
        symbol="DEVO.L",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Frontier Developments",
        symbol="FDEV.L",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="11 bit",
        symbol="11B.WA",
        steam_names=[],
        rawg_name="",
    ),
    src.models.publisher.PublisherId(
        name="Remedy",
        symbol="REMEDY.HE",
        steam_names=[],
        rawg_name="",
    ),
]


def main() -> None:
    """
    Main function to collect, format and export data to JSON.
    """
    src.echo.echoInfo("Bienvenue dans notre collecteur de données de jeux vidéo !")

    ###############
    # User inputs #
    ###############

    # Output file
    src.echo.echoInput("Nom du fichier de sortie (Laisser vide pour 'dataset.json')")
    user_input = input().strip() or "dataset.json"

    if not user_input.lower().endswith(".json"):
        user_input += ".json"

    path: pathlib.Path = pathlib.Path(user_input)

    if not path.parent.exists():
        src.echo.echoError(f"Le répertoire spécifié n'existe pas : {path.parent}")
        return

    try:
        path.name
        path.touch(exist_ok=True)
    except (OSError, ValueError):
        src.echo.echoError(f"Le nom de fichier spécifié n'est pas valide pour ce système d'exploitation : {path.name}")
        return

    src.echo.echoInfo(f"Le fichier de sortie sera : {path.resolve()}")

    # Select publishers
    src.echo.echoInput("Combien de publishers voulez-vous collectés ? (Sélection aléatoire) (Laisser vide pour tous)", is_one_line=True)
    user_input = input().strip()

    if user_input.isdigit():
        selected_publishers = random.sample(PUBLISHERS, min(int(user_input), len(PUBLISHERS)))
    else:
        src.echo.echoInfo(f"Aucun nombre spécifié, collecte de tous les publishers ({len(PUBLISHERS)})")
        selected_publishers = PUBLISHERS

    # Max games per publisher
    src.echo.echoInput("Combien de jeux maximum par publisher ? (Laisser vide pour tous)", is_one_line=True)
    user_input = input().strip()

    if user_input.isdigit():
        steam_max_games_per_publisher = int(user_input)
    else:
        src.echo.echoInfo(f"Aucun nombre spécifié, collecte de tous les publishers ({len(PUBLISHERS)})")
        steam_max_games_per_publisher = None

    ###################
    # Data collection #
    ###################

    data: list[src.models.Data] = src.getData(
        publishers_ids=selected_publishers,
        steam_max_games_per_publisher=steam_max_games_per_publisher,
        rawg_key=os.getenv("RAWG_API_KEY", ""),
    )

    src.echo.echoInfo("Collecte de données terminée.")
    src.echo.echoInfo(f"Nombre total de jeux collectés : {len(data)}")

    ##################
    # Export to JSON #
    ##################

    # Convert to JSON-serializable format
    json_data = [d.toDict() for d in data]

    # Export to JSON file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=True)

    src.echo.echoInfo("Exportation des données terminée.")
    src.echo.echoInfo(f"Fichier exporté : {len(json_data)} entrées sauvegardées dans {path.resolve()}")

    ##########################
    # Post-export statistics #
    ##########################

    # Display some statistics
    with_notes = sum(1 for d in data if d.note is not None)

    src.echo.echoInfo("Statistiques :")
    src.echo.echoInfo(f"- Jeux collectés : {len(data)}", indent=1)
    src.echo.echoInfo(f"- Jeux avec notes : {with_notes}/{len(data)}", indent=1)


if __name__ == "__main__":
    main()
