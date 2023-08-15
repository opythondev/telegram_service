from telethon import TelegramClient
from bot.configs.env import CLIENTS

client = TelegramClient('9165798836',
                        CLIENTS['client'][0], CLIENTS['client'][1]).start()
client2 = TelegramClient('9165797221',
                         CLIENTS['client2'][0], CLIENTS['client2'][1]).start()
