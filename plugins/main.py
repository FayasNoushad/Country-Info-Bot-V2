import os
from countryinfo import CountryInfo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from .database import db


START_TEXT = """Hello {} 😌
I am a country information finder bot.

>> `I can find information of any country of the world.`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

➠ Just send me a country name 
➠ Then I will check and send you the informations

**Available Commands**

/start - Checking Bot Online
/help - For more help
/about - For more about me
/status - For bot status

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me**-- 😎

🤖 **Name :** [Country Info Bot](https://telegram.me/{})

👨‍💻 **Developer :** [Fayas](https://github.com/FayasNoushad)

📢 **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)

🌐 **Source :** [👉 Click here](https://github.com/FayasNoushad/Country-Info-Bot-V2)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⚙ Help', callback_data='help'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('Help ⚙', callback_data='help'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

ERROR_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⚙ Help', callback_data='help'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)


@Client.on_callback_query()
async def cb_handler(bot, update):

    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )

    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )

    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )

    else:
        await update.message.delete()


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):

    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):

    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await update.reply_text(
        text=HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
    )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):

    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


def country_info(country):
    country = CountryInfo(country)
    info = f"""\
Name : `{country.name()}`
Native Name : `{country.native_name()}`
Capital : `{country.capital()}`
Population : `{country.population()}`
Region : `{country.region()}`
Sub Region : `{country.subregion()}`
Top Level Domains : `{country.tld()}`
Calling Codes : `{country.calling_codes()}`
Currencies : `{country.currencies()}`
Residence : `{country.demonym()}`
Timezone : `{country.timezones()}`"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Wikipedia', url=country.wiki()),
                InlineKeyboardButton('Google', url=country.google())
            ],
            [
                InlineKeyboardButton('Join Channel', url='https://telegram.me/FayasNoushad')
            ]
        ]
    )
    return info, buttons


@Client.on_message(filters.private & filters.text)
async def countryinfo(bot, update):

    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    if update.text.startswith("/"):
        return

    info, buttons = country_info(update.text)

    try:
        await bot.send_message(
            chat_id=update.chat.id,
            text=info,
            reply_markup=buttons,
            disable_web_page_preview=True,
            reply_to_message_id=update.message_id
        )
    except Exception as error:
        print(error)


@Client.on_inline_query()
async def countryinfo_inline(bot, update):

    join_channel_text = "Please join my channel for more bots and updates"
    channel_reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton('😎 Join Channel 😎', url='https://telegram.me/FayasNoushad')]]
    )

    info, buttons = country_info(update.query)

    if update.query == "":
        answers = [
            InlineQueryResultArticle(
                title="Join Channel 😎",
                description=join_channel_text,
                input_message_content=InputTextMessageContent(join_channel_text),
                reply_markup=channel_reply_markup
            )
        ]
    else:
        answers = [
            InlineQueryResultArticle(
                title=update.query,
                description=f"Information of {update.query}",
                input_message_content=InputTextMessageContent(info),
                reply_markup=buttons
            )
        ]

    await bot.answer_inline_query(
        inline_query_id=update.chat.id,
        results=answers
    )


@Client.on_message(filters.private & filters.command("status"), group=5)
async def status(bot, update):

    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"

    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )
