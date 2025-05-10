import json
from telegram.ext import Updater, CommandHandler  # et les autres imports que tu utilises
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import json
def lire_solde(user_id):
    with open('soldes.json', 'r') as file:
        soldes = json.load(file)
    return soldes.get(str(user_id), 0)

def mettre_a_jour_solde(user_id, montant):
    with open('soldes.json', 'r') as file:
        soldes = json.load(file)

    user_id = str(user_id)
    soldes[user_id] = soldes.get(user_id, 0) + montant

    with open('soldes.json', 'w') as file:
        json.dump(soldes, file)
# Remplace par ton propre token
TOKEN = "8151164658:AAGcGdTauzNoozJZRO60htExQs2kiKBJmwE"
ADMIN_ID = 6406991534  # remplace par TON VRAI ID TELEGRAM

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bienvenue ! Utilise /solde pour voir ton solde.")

def solde(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)

    try:
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
    except:
        soldes = {}

    montant = soldes.get(user_id, 0)
    update.message.reply_text(f"Ton solde est de {montant} FCFA.")

def retrait(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Inconnu"

    if len(context.args) != 1 or not context.args[0].isdigit():
        update.message.reply_text("Utilise comme ceci : /retrait 1000")
        return

    montant = int(context.args[0])

    try:
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
    except:
        soldes = {}

    solde = soldes.get(user_id, 0)

    if montant > solde:
        update.message.reply_text("Fonds insuffisants.")
        return

    soldes[user_id] -= montant

    with open("soldes.json", "w") as f:
        json.dump(soldes, f)

    update.message.reply_text(f"Demande de retrait de {montant} FCFA envoyée.")

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Demande de retrait de {montant} FCFA par @{username} (ID: {user_id})"
    )

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("solde", solde))
    dispatcher.add_handler(CommandHandler("retrait", retrait))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
