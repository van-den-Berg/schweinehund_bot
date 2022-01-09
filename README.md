# Schweinehund

The aim of this Telegram Bot is to help the members of a group achieve their goals for 2022.
It acts as a habbit tracker and makes the habbit tracking a social thing, applying peer-pressure.


## Requirements
- Python 3.7


    pip install pyTelegramBotAPI python-telegram-bot --upgrade


## Notes

### ToDo:
- locks auf dateien ausweiten. bis jetzt wird nur während schreiben/lesen gelocked. theoretisch muss aber gelocked werden wenn etwas am Zustand von data_obj geändert wird.
- Habbits:
  - wenn man Bot privat schreibt, das man eine Aufgabe gemacht hat sollte es in allen Gruppen ankommen in denen man ist
  - Habbits müssen in Gruppe und privatem chat als gemacht setzbar sein
- Accounting:
  - es sollte einen Befehl für Zusammenfassung/ aktuellen Stand in der Woche geben. 
- einige Nachrichten sollten nach einer bestimmten Zeit wieder verschwinden

### Ignore Config File
- We do not want our Token (from the config.json file) in Git Commits.
    
    
    git update-index --skip-worktree config.json

- to put the file back into the worktree (be sure there is no Token in there !!!:
  
    
    git update-index --no-skip-worktree config.json
