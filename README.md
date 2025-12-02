# ET4-DATA-ENGINEERING-PROJECT-DATASET

Projet 1 du module "Ingénierie des données" de l'ET4-IIM, Polytech Paris-Saclay.

Le but de ce projet est de créer un nouveau dataset à partir de datasets existants ou d'API publiques, en utilisant des techniques d'ingénierie des données pour collecter, nettoyer, transformer et enrichir les données.

---

## Contents

- [Usage](#usage)
  - [Installation](#installation)
  - [Running](#running)
- [Structure](#structure)
- [Git Commands](#git-commands)

---

## Usage

- ### Installation
  1. need to clone the repository : run `git clone https://github.com/MES4game/ET4-DATA-ENGINEERING-PROJECT-DATASET project-dataset` to clone it in a folder named `project-dataset`
  2. run `cd project-dataset` to navigate to the cloned repository
  3. be sure to have installed Python 3.12 or higher and pip
  4. run `pip install -r requirements.txt` to install the dependencies

- ### Running
  1. run `python3 main.py` to launch the application
  2. follow the instructions in the terminal to use the application

---

## Structure

- `src`: source code (Python scripts)
- `.gitignore`: files to ignore by git
- `LICENSE`: license file (MIT)
- `main.py`: main entry point of the application
- `requirements.txt`: list of dependencies
- `README.md`: this file

---

## Git Commands

- `git status`: check the status of the repository
- `git fetch origin`: fetch changes from remote
- `git checkout <branch>`: switch to an existing branch
- `git pull origin`: pull changes from remote branch
- `git add .`: stage all changes
- `git add <file>...`: stage specific file (can use glob patterns)
- `git commit -m "<commit message>"`: commit staged changes with a message
- `git push origin`: push changes to remote branch
- `git stash -u`: stash changes (to be reapplied later, for example when switching branch)
- `git stash pop`: reapply stashed changes
