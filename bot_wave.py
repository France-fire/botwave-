import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# Ton token et ID admin
TOKEN = "8151164658:AAGcGdTauzNoozJZRO60htExQs2kiKBJmwE"
ADMIN_ID = 6406991534  # remplace par ton vrai ID Telegram

# Lire le solde d'un utilisateur
def lire_solde(user_id):
    try:
        with open('soldes.json', 'r') as file:
            soldes = json.load(file)
    except:
        soldes = {}
    return soldes.get(str(user_id), 0)

# Mettre à jour le solde d'un utilisateur
def mettre_a_jour_solde(user_id, montant):
    try:
        with open('soldes.json', 'r') as file:
            soldes = json.load(file)
    except:
        soldes = {}

    user_id = str(user_id)
    soldes[user_id] = soldes.get(user_id, 0) + montant

    with open('soldes.json', 'w') as file:
        json.dump(soldes, file)

# Commande /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bienvenue ! Utilise /solde pour voir ton solde.")

# Commande /solde
def solde(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    montant = lire_solde(user_id)
    update.message.reply_text(f"Ton solde est de {montant} FCFA.")

# Commande /retrait
def retrait(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Inconnu"

    if len(context.args) != 1 or not context.args[0].isdigit():
        update.message.reply_text("Utilise comme ceci : /retrait 1000")
        return

    montant = int(context.args[0])
    solde_actuel = lire_solde(user_id)

    if montant > solde_actuel:
        update.message.reply_text("Fonds insuffisants.")
        return

    mettre_a_jour_solde(user_id, -montant)

    update.message.reply_text(f"Demande de retrait de {montant} FCFA envoyée.")

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Demande de retrait de {montant} FCFA par @{username} (ID: {user_id})"
    )

# Lancement du bot
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
