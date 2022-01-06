# Schweinehund

The aim of this Telegram Bot is to help the members of a group achieve their goals for 2022.
It acts as a habbit tracker and makes the habbit tracking a social thing, applying peer-pressure.


## Requirements
- Python 3.7


    pip install pyTelegramBotAPI python-telegram-bot --upgrade

## Notes

### ToDo:
- speichere die Chatgruppe in den User, Bot kann in mehreren Gruppen gleichzeitig sein
- JSON um Daten persistent zu speichern (falls server down geht)
  - im JSON Trennung nach USER Daten und Habbit Daten
- Bot kann in mehreren Gruppen gleichzeitig sein. an Chat ID kann unterschieden werden wo Nachricht her kommt. 
  - wenn man Bot privat schreibt das man eine Aufgabe gemacht hat sollte es in allen Gruppen ankommen
- 

### Ignore Config File
- We do not want our Token (from the config.json file) in Git Commits.
    
    
    git update-index --skip-worktree config.json

- to put the file back into the worktree (be sure there is no Token in there !!!:
  
    
    git update-index --no-skip-worktree config.json
