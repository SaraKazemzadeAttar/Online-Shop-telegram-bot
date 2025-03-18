import telebot
import os
from Models import db 
import re
# CHANNEL_ID = os.environ.get("CHANNEL_ID")
# CHANNEL_LINK = os.environ.get("CHANNEL_LINK")

def register(bot):


    def is_member(bot , message):
        if not bot:
            return False

        user_info = bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if user_info.status not in ["administrator", "creator", "member"]:
            bot.send_message(
                message.chat.id,
                f"⚠️ Please subscribe to our channel to use this bot: [Join Channel]({CHANNEL_LINK})",
                parse_mode="Markdown",
            )
            return False
        return True

    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.chat.id
        user = db.users_collection.find_one({"_id": user_id})

        if not user:
            db.users_collection.insert_one({"_id": user_id, "cart": []})
            bot.send_message(user_id, "👋 Welcome! use /register to create your account" )
        else:
            bot.send_message(user_id, "👋 Welcome back!")

        bot.send_message(user_id, "🛒 Use /cart to view your shopping cart.\n💳 Use /pay to proceed to payment.")
        
    def is_registered(user_id):
        return db.users_collection.find_one({"user_id": user_id}) is not None

    @bot.message_handler(commands=["register"])
    def setup_name(message):
        user_id = message.chat.id
        if is_registered(user_id):
            bot.send_message(user_id, "🚀 You are already registered!")
            return
        
        bot.send_message(user_id, "Please enter your first name:")
        bot.register_next_step_handler(message, ask_contact)

    def ask_contact(message):
        fname = message.text.strip()
        if not fname:
            bot.send_message(message.chat.id, "❌ First name cannot be empty. Try again.")
            bot.register_next_step_handler(message, ask_contact)
            return

        bot.send_message(message.chat.id, "Please enter your phone number (09123456789) or email (example@gmail.com):")
        bot.register_next_step_handler(message, set_user, fname)

    def set_user(message, fname):
        contact = message.text.strip()
        
        # Validate phone number
        if contact.startswith("09") and contact[1:].isdigit():
            phone = contact
            email = None
        # Validate email
        elif re.match(r"[^@]+@[^@]+\.[^@]+", contact):
            email = contact
            phone = None
        else:
            bot.send_message(message.chat.id, "❌ Invalid phone number or email format. Try again:")
            bot.register_next_step_handler(message, set_user, fname)
            return

        db.insert_user(user_id=message.chat.id, first_name=fname, phone=phone, email=email, username=message.chat.username)
        
        bot.send_message(message.chat.id, f"✅ Dear {fname}, your registration is complete!\nThanks for using this bot. 🤝")
