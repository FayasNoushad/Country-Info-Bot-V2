import vars
from pyrogram import Client


Bot = Client(
    vars.SESSION_NAME,
    bot_token=vars.BOT_TOKEN,
    api_id=int(vars.API_ID),
    api_hash=vars.API_HASH,
    plugins=dict(root="plugins")
)


Bot.run()
