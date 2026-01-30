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
import datetime
import src


dotenv.load_dotenv()


PUBLISHERS: list[src.models.publisher.PublisherId] = [
    src.models.publisher.PublisherId(
        name="Ubisoft",
        symbol="UBI.PA",
        steam_names=["Ubisoft"],
        rawg_name="ubisoft-entertainment",
    ),
    src.models.publisher.PublisherId(
        name="Capcom",
        symbol="9697.T",
        steam_names=["CAPCOM Co., Ltd.", "CAPCOM"],
        rawg_name="capcom",
    ),
    src.models.publisher.PublisherId(
        name="Electronic Arts",
        symbol="EA",
        steam_names=["Electronic Arts"],
        rawg_name="electronic-arts",
    ),
    src.models.publisher.PublisherId(
        name="Square Enix",
        symbol="9684.T",
        steam_names=["Square Enix"],
        rawg_name="square-enix",
    ),
    src.models.publisher.PublisherId(
        name="Microsoft",
        symbol="MSFT",
        steam_names=["Xbox Game Studios"],
        rawg_name="microsoft-studios",
    ),
    src.models.publisher.PublisherId(
        name="Sega Sammy",
        symbol="6460.T",
        steam_names=["SEGA"],
        rawg_name="sega-2",
    ),
    src.models.publisher.PublisherId(
        name="Warner Bros. Discovery",
        symbol="WBD",
        steam_names=["Warner Bros. Games"],
        rawg_name="warner-bros-interactive",
    ),
    src.models.publisher.PublisherId(
        name="Sony",
        symbol="SONY",
        steam_names=["PlayStation Publishing LLC"],
        rawg_name="sony-interactive-entertainment",
    ),
    src.models.publisher.PublisherId(
        name="Bandai Namco",
        symbol="7832.T",
        steam_names=["Bandai Namco Entertainment Inc."],
        rawg_name="bandai-namco-entertainment",
    ),
    src.models.publisher.PublisherId(
        name="Take-Two Interactive",
        symbol="TTWO",
        steam_names=["Rockstar Games", "2K"],
        rawg_name="take-two-interactive",
    ),
    src.models.publisher.PublisherId(
        name="Konami",
        symbol="9766.T",
        steam_names=["KONAMI"],
        rawg_name="konami",
    ),
    src.models.publisher.PublisherId(
        name="CDProjekt",
        symbol="CDR.WA",
        steam_names=["CD PROJEKT RED"],
        rawg_name="cd-projekt-red",
    ),
    src.models.publisher.PublisherId(
        name="Koei Tecmo",
        symbol="3635.T",
        steam_names=["KOEI TECMO GAMES CO., LTD."],
        rawg_name="koei-tecmo-games",
    ),
]


def main() -> None:
    """
    Main function to collect, format and export data to JSON.
    """
    src.utils.echoInfo("Bienvenue dans notre collecteur de données de jeux vidéo !")

    ###############
    # User inputs #
    ###############

    # Output file
    src.utils.echoInput("Nom du fichier de sortie (Laisser vide pour 'dataset.json')")
    user_input = input().strip() or "dataset.json"

    if not user_input.lower().endswith(".json"):
        user_input += ".json"

    path: pathlib.Path = pathlib.Path(user_input)

    if not path.parent.exists():
        src.utils.echoError(f"Le répertoire spécifié n'existe pas : {path.parent}")
        return

    try:
        path.name
        path.touch(exist_ok=True)
    except (OSError, ValueError):
        src.utils.echoError(f"Le nom de fichier spécifié n'est pas valide pour ce système d'exploitation : {path.name}")
        return

    src.utils.echoInfo(f"Le fichier de sortie sera : {path.resolve()}")

    # Select publishers
    src.utils.echoInput("Combien de publishers voulez-vous collectés ? (Sélection aléatoire) (Laisser vide pour tous)")
    user_input = input().strip()

    if user_input.isdigit():
        selected_publishers = random.sample(PUBLISHERS, min(int(user_input), len(PUBLISHERS)))
        src.utils.echoInfo(f"Collecte de {len(selected_publishers)} publishers sélectionnés aléatoirement.")
    else:
        src.utils.echoInfo(f"Aucun nombre spécifié, collecte de tous les publishers ({len(PUBLISHERS)})")
        selected_publishers = PUBLISHERS

    # Max games per publisher
    src.utils.echoInput("Combien de jeux maximum par publisher ? (Laisser vide pour tous)")
    user_input = input().strip()

    if user_input.isdigit():
        steam_max_games_per_publisher = int(user_input)
        src.utils.echoInfo(f"Limite de {steam_max_games_per_publisher} jeux par publisher.")
    else:
        src.utils.echoInfo(f"Aucun nombre spécifié, collecte de tous les publishers ({len(PUBLISHERS)})")
        steam_max_games_per_publisher = None

    # Min score for name similarity
    src.utils.echoInput("Quel score minimal pour accepter la similarité des noms ? (0.0 - 1.0) (Laisser vide pour 0.6)")
    user_input = input().strip()

    try:
        min_score_similarity = float(user_input)
        min_score_similarity = max(0.0, min(1.0, min_score_similarity))
        src.utils.echoInfo(f"Score minimal de similarité des noms défini à {min_score_similarity}")
    except ValueError:
        src.utils.echoInfo("Aucun score spécifié, utilisation de la valeur par défaut (0.6)")
        min_score_similarity = 0.6

    ###################
    # Data collection #
    ###################

    data_collect_start_time: str = datetime.datetime.now().isoformat()

    data: list[src.models.Data] = src.getData(
        publishers_ids=selected_publishers,
        steam_max_games_per_publisher=steam_max_games_per_publisher,
        rawg_key=os.getenv("RAWG_API_KEY", ""),
        min_score_similarity=min_score_similarity,
    )

    src.utils.echoInfo("Collecte de données terminée.")
    src.utils.echoInfo(f"Nombre total de jeux collectés : {len(data)}")

    ##################
    # Export to JSON #
    ##################

    # Convert to JSON-serializable format
    json_data = [d.toDict(data_collect_start_time) for d in data]

    # Export to JSON file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=True)

    src.utils.echoInfo("Exportation des données terminée.")
    src.utils.echoInfo(f"Fichier exporté : {len(json_data)} entrées sauvegardées dans {path.resolve()}")

    ##########################
    # Post-export statistics #
    ##########################

    # Display some statistics
    with_notes = sum(1 for d in data if d.note is not None)

    src.utils.echoInfo("Statistiques :")
    src.utils.echoInfo(f"- Jeux collectés : {len(data)}", indent=1)
    src.utils.echoInfo(f"- Jeux avec notes : {with_notes}/{len(data)}", indent=1)


if __name__ == "__main__":
    main()
