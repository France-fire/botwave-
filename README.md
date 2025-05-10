# BotWave Telegram Bot

Un bot Telegram qui permet de :

- Consulter son solde avec `/solde`
- Faire une demande de retrait avec `/retrait montant`

## Fichiers

- `bot_wave.py` : Code principal du bot
- `soldes.json` : Stockage des soldes des utilisateurs
- `requirements.txt` : Dépendances Python
- `Procfile` : Utilisé pour l’hébergement sur Railway ou Heroku

## Lancer le bot dans Termux

```bash
pkg update && pkg install git python
pip install -r requirements.txt
git clone https://github.com/France-fire/botwave-.git
cd botwave-
python bot_wave.py
