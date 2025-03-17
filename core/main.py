import telebot
import os
import logging
import importlib
import importlib.util
import sys

logger = telebot.logger

telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

sys.path.append(os.path.dirname(__file__))

handlers_dir = os.path.join(os.path.dirname(__file__), 'handlers')
Models_dir =  os.path.join(os.path.dirname(__file__), 'handlers')

for file in os.listdir(handlers_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = f"handlers.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(handlers_dir, file))
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        if hasattr(module, 'register'):
            module.register(bot)
            
for file in os.listdir(Models_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = f"Models.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(Models_dir, file))
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        if hasattr(module, 'register'):
            module.register(bot)

bot.infinity_polling()