import telebot
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["telegram_bot"] 
cart_collection = db["carts"]
order_collection = db["orders"]


TEST_PRODUCTS = [
    {"id": "1", "name": "bag", "price": 500000},
    {"id": "2", "name": "Samsung Galaxy A73", "price": 27000000},
    {"id": "3", "name": "notebook", "price": 200000},
]
def register(bot):
    @bot.message_handler(commands=['products'])
    def show_products(message):
        markup = InlineKeyboardMarkup()

        for product in TEST_PRODUCTS:
            button = InlineKeyboardButton(
                text=f"{product['name']} - تومان {product['price']}",
                callback_data=f"add_{product['id']}"
            )
            markup.add(button)

        bot.send_message(message.chat.id, "🛍️ Choose a product to add to your cart:", reply_markup=markup)
        
    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
    def handle_add_to_cart(call):
        user_id = call.message.chat.id
        product_id = call.data.split("_")[1]

        product = next((p for p in TEST_PRODUCTS if p["id"] == product_id), None)
        if not product:
            bot.answer_callback_query(call.id, "❌ Product not found.")
            return

        cart_collection.update_one(
            {"user_id": user_id},
            {"$push": {"products": f"{product['name']} - ${product['price']}"}},
            upsert=True
        )

        bot.answer_callback_query(call.id, f"✅ {product['name']} added to cart!")

    @bot.message_handler(commands=['add'])
    def add_to_cart_cmd(message):
        user_id = message.chat.id
        msg = message.text.split()

        if len(msg) < 2:
            product_list = "\n".join([f"{p['id']}: {p['name']} - ${p['price']}" for p in TEST_PRODUCTS])
            bot.send_message(user_id, "Available Products:\n" + product_list + "\n\nUsage: /add <product_id>")
            return

        product_id = msg[1]
        product = next((p for p in TEST_PRODUCTS if p["id"] == product_id), None)

        if not product:
            bot.reply_to(message, "❌ Invalid product ID.")
            return

        cart_collection.update_one(
            {"user_id": user_id},
            {"$push": {"products": f"{product['name']} - ${product['price']}"}},
            upsert=True
        )

        bot.reply_to(message, f"✅ Product *{product['name']}* has been added to your cart.", parse_mode="Markdown")

    # Remove product
    @bot.message_handler(commands=['remove'])
    def remove_from_cart(message):
        user_id = message.chat.id
        product = message.text.replace("/remove", "").strip()

        if not product:
            bot.reply_to(message, "❌ Please enter the product name to remove.")
            return

        cart_collection.update_one(
            {"user_id": user_id},
            {"$pull": {"products": product}}
        )

        bot.reply_to(message, f"🗑️ Product *{product}* removed from your cart.", parse_mode="Markdown")

    # View cart
    @bot.message_handler(commands=['review'])
    def view_cart(message):
        user_id = message.chat.id
        cart = cart_collection.find_one({"user_id": user_id})

        if not cart or "products" not in cart or len(cart["products"]) == 0:
            bot.reply_to(message, "🛒 Your cart is empty.")
            return

        cart_items = "\n".join([f"- {item}" for item in cart["products"]])
        bot.reply_to(message, f"*Your Cart:*\n{cart_items}\n\n✅ To confirm your order, type /confirm", parse_mode="Markdown")

    @bot.message_handler(commands=['confirm'])
    def confirm_order(message):
        user_id = message.chat.id
        cart = cart_collection.find_one({"user_id": user_id})

        if not cart or "products" not in cart or len(cart["products"]) == 0:
            bot.reply_to(message, "🛒 Your cart is empty.")
            return

        cart_items = "\n".join([f"- {item}" for item in cart["products"]])
        bot.reply_to(message, f"✅ Your order has been confirmed:\n{cart_items}\n\n💳 Processing payment...")

        order_collection.insert_one({
            "user_id": user_id,
            "products": cart["products"],
            "status": "Pending Payment"
        })

        cart_collection.delete_one({"user_id": user_id})

        payment_url = "https://sandbox.zarinpal.com/pg/StartPay/00000000-0000-0000-0000-000000000000"
        bot.send_message(user_id, f"[🧾 Pay Now]({payment_url})", parse_mode="Markdown")
