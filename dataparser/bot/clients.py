from telethon import TelegramClient
from bot.configs.env import CLIENTS

client = TelegramClient('anon', CLIENTS['client'][0], CLIENTS['client'][1]).start()
client2 = TelegramClient('client2', CLIENTS['client2'][0], CLIENTS['client2'][1]).start()
client3 = TelegramClient('client3', CLIENTS['client3'][0], CLIENTS['client3'][1]).start()








