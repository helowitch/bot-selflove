from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import openai
import os
import logging

# Ton token Telegram
TOKEN = "7468439207:AAGlsyi_i0A40TtXA_rJX_c0M84bQUYYbHE"
# Ton API Key Mistral
MISTRAL_API_KEY = "h7NG4OH6aBj9Nww2oUfdLQuyTvVMsB4r"

# ID du groupe Telegram
CHAT_ID = "-1001267100130"

# Initialize OpenAI API
openai.api_key = MISTRAL_API_KEY

# Test de l'initialisation
def test_initialization():
    if not TOKEN or not MISTRAL_API_KEY:
        print("Erreur: Token ou clé API manquants !")
        return False
    print("Initialisation réussie !")
    return True

# Vérifier l'initialisation avant de lancer le bot
if __name__ == "__main__":
    if test_initialization():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logger = logging.getLogger(__name__)
        main()


async def generate_compliment():
    """Génère un compliment avec l'IA Mistral."""
    prompt = "Génère un compliment sincère, chaleureux et mignon, non genré, pour une personne."

    response = openai.Completion.create(
        engine="mistral-7b",
        prompt=prompt,
        max_tokens=60
    )
    
    compliment = response.choices[0].text.strip()
    return compliment

async def send_compliment(update: Update, context: CallbackContext):
    """Envoie un compliment en réponse à la commande /weewoo."""
    compliment = await generate_compliment()
    message = f"🚨🚓🚨WEE WOO !!! POLICE DU SELF-LOVE !!\n{compliment}"
    await update.message.reply_text(message)

async def handle_message(update: Update, context: CallbackContext):
    """Envoie un compliment tous les 500 messages."""
    user_message_count = context.bot_data.get('message_count', 0)
    user_message_count += 1
    context.bot_data['message_count'] = user_message_count

    if user_message_count % 500 == 0:
        compliment = await generate_compliment()
        message = f"🚨🚨POLICE DU SELF-LOVE ! INTERVENTION SURPRISE !\n{compliment}"
        await update.message.reply_text(message)

async def main():
    application = Application.builder().token(TOKEN).build()

    # Ajouter la gestion des messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Ajouter la gestion de la commande /weewoo
    application.add_handler(CommandHandler("weewoo", send_compliment))

    # Lancer l'application
    await application.run_polling()

# Lancer le bot sans asyncio.run(), l'environnement gère déjà la boucle d'événements
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Appel direct de la fonction main, sans asyncio.run()
    main()  # La boucle d'événements est gérée par la bibliothèque telegram.ext
