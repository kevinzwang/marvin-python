# Marvin
A bot to manage the Discord Chaos server.

## Requirements
Currently only works on Python 3.5.*

To use, first do:
```
pip install discord.py[voice]
pip install PyYAML
```
and also follow the instructions [here](https://github.com/Just-Some-Bots/MusicBot/wiki) to configure music.

## Versions

### 1.0.0
* First official version! Features:
* "I'm __" responds with "Hi __!" and changes nickname for 30 seconds
* Reacting with '📌' to a message pins it, and removing it unpins it
* *lmgtfy* - sends a lmgtfy.com link with query specified
* *ping* - pings bot and gets time the ping took to send
* *opt* - opts in our out of the "I'm __" feature
* *available/avail* - specifies that you are available for game night.
⋅⋅⋅If 4 or more people are at one time, Marvin mentions them for game night.
* *truth/dare/wyr* - chooses randomly one of the tord questions to send in the yaml/tord.yaml file.
* *prefix* - allows you to view and change the command prefix
* *quit* - quits the bot safely with option to dump data
* *restart* - restarts the bot safely with option to dump data
* *dump* - only dumps data