from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import json
import requests

# --- Config ---
TOKEN = "8151164658:AAGcGdTauzNoozJZRO60htExQs2kiKBJmwE"
ADMIN_ID = 6406991534
DJAMO_EMAIL = "ton@email.com"
DJAMO_PASSWORD = "ton_mot_de_passe"

# --- Fonctions API Djamo ---
def se_connecter_djamo():
    url = "https://api.djamo.com/auth/login"  # À adapter
    data = {"email": DJAMO_EMAIL, "password": DJAMO_PASSWORD}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["token"]

def envoyer_virement_djamo(token, destinataire, montant):
    url = "https://api.djamo.com/transfer"  # À adapter
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "receiver_identifier": destinataire,
        "amount": montant
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# --- Utilitaires solde ---
def lire_solde(user_id):
    try:
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
        return soldes.get(str(user_id), 0)
    except:
        return 0

def mettre_a_jour_solde(user_id, montant):
    try:
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
    except:
        soldes = {}

    user_id = str(user_id)
    soldes[user_id] = soldes.get(user_id, 0) + montant

    with open("soldes.json", "w") as f:
        json.dump(soldes, f)

# --- Commandes Telegram ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bienvenue ! Utilise /solde pour voir ton solde.")

def solde(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    montant = lire_solde(user_id)
    update.message.reply_text(f"Ton solde est de {montant} FCFA.")

def set_djamo(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)

    if len(context.args) != 1:
        update.message.reply_text("Utilise comme ceci : /setdjamo identifiant_djamo")
        return

    identifiant = context.args[0]

    try:
        with open("djamo_ids.json", "r") as f:
            ids = json.load(f)
    except:
        ids = {}

    ids[user_id] = identifiant

    with open("djamo_ids.json", "w") as f:
        json.dump(ids, f)

    update.message.reply_text(f"Identifiant Djamo enregistré : {identifiant}")

def retrait(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Inconnu"

    if len(context.args) != 1 or not context.args[0].isdigit():
        update.message.reply_text("Utilise comme ceci : /retrait 1000")
        return

    montant = int(context.args[0])
    solde = lire_solde(user_id)

    if montant > solde:
        update.message.reply_text("Fonds insuffisants.")
        return

    try:
        with open("djamo_ids.json", "r") as f:
            ids = json.load(f)
        identifiant_djamo = ids.get(user_id, None)
    except:
        identifiant_djamo = None

    if not identifiant_djamo:
        update.message.reply_text("Tu dois d'abord enregistrer ton identifiant Djamo avec /setdjamo.")
        return

    # Déduire le solde
    mettre_a_jour_solde(user_id, -montant)
    update.message.reply_text("Traitement de ton retrait en cours...")

    # Envoi automatique via Djamo
    try:
        token = se_connecter_djamo()
        resultat = envoyer_virement_djamo(token, identifiant_djamo, montant)

        context.bot.send_message(
            chat_id=user_id,
            text=f"Ton retrait de {montant} FCFA a été effectué via Djamo."
        )
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Retrait automatique de {montant} FCFA effectué pour {username} ({user_id}) vers {identifiant_djamo}."
        )
    except Exception as e:
        context.bot.send_message(chat_id=user_id, text=f"Erreur lors de l'envoi via Djamo : {e}")
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Erreur lors du retrait de {username} : {e}")
        mettre_a_jour_solde(user_id, montant)  # Recréditer en cas d'échec

# --- Main ---
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("solde", solde))
    dispatcher.add_handler(CommandHandler("retrait", retrait))
    dispatcher.add_handler(CommandHandler("setdjamo", set_djamo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
