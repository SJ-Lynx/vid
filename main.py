import os
import ytthumb
import requests
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


Bot = Client(
    "YouTube-Search-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.all)
async def text(bot, update):
    text = "Поиск видео на YouTube с помощью кнопок ниже."
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Канал", url="https://t.me/SJa_Bots")] 
            [InlineKeyboardButton(text="Сообщать об ошибках 😊", url="https://t.me/SJ_Lynx")]
            [InlineKeyboardButton(text="Искать здесь", switch_inline_query_current_chat="")],
            [InlineKeyboardButton(text="Поиск в другом чате", switch_inline_query="")]
        ]
    )
    await update.reply_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def search(bot, update):
    results = requests.get(
        "https://youtube.api.fayas.me/videos/?query=" + requote_uri(update.query)
    ).json()["result"][:50]
    answers = []
    for result in results:
        title = result["title"]
        views_short = result["viewCount"]["short"]
        duration = result["duration"]
        duration_text = result["accessibility"]["duration"]
        views = result["viewCount"]["text"]
        publishedtime = result["publishedTime"]
        channel_name = result["channel"]["name"]
        channel_link = result["channel"]["link"]
        description = f"{views_short} | {duration}"
        details = f"**Title:** {title}" + "\n" \
        f"**Канал:** [{channel_name}]({channel_link})" + "\n" \
        f"**Продолжительность:** {duration_text}" + "\n" \
        f"**Просмотры:** {views}" + "\n" \
        f"**Время публикации:** {publishedtime}" + "\n" \
        "\n" + "**Made by @SJ_Lynx**"
        thumbnail = ytthumb.thumbnail(result["id"])
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Смотреть Видео 📹", url=result["link"])]
            ]
        )
        try:
            answers.append(
                InlineQueryResultPhoto(
                    title=title,
                    description=description,
                    caption=details,
                    photo_url=thumbnail,
                    reply_markup=reply_markup
                )
            )
        except:
            pass
    await update.answer(answers)


Bot.run()
