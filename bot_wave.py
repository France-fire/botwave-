from telegram.ext import Updater, CommandHandler
import json
import os

TOKEN = "8151164658:AAGcGdTauzNoozJZRO60htExQs2kiKBJmwE"  # Remplace par ton token réel
solde_file = "soldes.json"

if os.path.exists(solde_file):
    with open(solde_file, "r") as f:
        soldes = json.load(f)
else:
    soldes = {}

def start(update, context):
    user_id = str(update.effective_user.id)
    if user_id not in soldes:
        soldes[user_id] = 0
        save()
    update.message.reply_text("Bienvenue ! Envoie /bonus pour recevoir ton bonus.")

def bonus(update, context):
    user_id = str(update.effective_user.id)
    soldes[user_id] = soldes.get(user_id, 0) + 650
    save()
    update.message.reply_text(f"Tu as reçu 650F ! Ton solde est maintenant de {soldes[user_id]} F.")

def solde(update, context):
    user_id = str(update.effective_user.id)
    montant = soldes.get(user_id, 0)
    update.message.reply_text(f"Ton solde est de {montant} F.")

def save():
    with open(solde_file, "w") as f:
        json.dump(soldes, f)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("bonus", bonus))
dp.add_handler(CommandHandler("solde", solde))

updater.start_polling()
updater.idle()
