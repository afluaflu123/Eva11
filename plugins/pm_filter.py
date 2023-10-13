# Kanged From @TroJanZheX
import asyncio
import re
import ast
import math
import random
import pytz
import datetime
import time
import psutil, shutil, sys
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, FILE_CHANNEL, CUSTOM_FILE_CAPTION, LOG_CHANNEL, AUTH_GROUPS, REQ_CHANNEL, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, PICS, FILE_FORWARD, SPELL_IMG, MAIN_CHANNEL, IMDB_TEMPLATE, NOR_IMG
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
from database.gfilters_mdb import (
    find_gfilter,
    get_gfilters,
    del_allg
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
BOT_START_TIME = time.time()
CLICK = {}

max_clicks = 1

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
        glob = await global_filters(client, message)
        if glob == False:
            manual = await manual_filters(client, message)
            if manual == False:
               await auto_filter(client, message)

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore♀️ommands and hashtags
    if user_id in ADMINS: return # ignore admins
    k = await message.reply_text(
         text="<b><i>ʜᴇʏ ᴅᴜᴅᴇ, ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ᴍᴏᴠɪᴇs ꜰʀᴏᴍ ʜᴇʀᴇ. ʀᴇǫᴜᴇsᴛ ᴏɴ ᴏᴜʀ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ ᴏʀ ᴄʟɪᴄᴋ ʀᴇǫᴜᴇsᴛ ʜᴇʀᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ​</i>👇</b>",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎗️ ʀᴇǫᴜᴇsᴛ ʜᴇʀᴇ​ 🎗️", url=f"https://t.me/KLMovieGroup")]]))
    await asyncio.sleep(15)
    await k.delete()
    await message.delete()
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>🍀 Pᴍ Mᴇssᴀɢᴇ ☘️\n\n📝 Mᴇssᴀɢᴇ ​:- {content}\n\n🤷 RᴇQᴜᴇꜱᴛᴇᴅ Bʏ :- {user}\n\n😋 Uꜱᴇʀ Iᴅ :- {user_id}</b>"
    )

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"★ {get_size(file.file_size)} ⊳ {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]
    btn.insert(0, 
        [
            InlineKeyboardButton(f'⇓ {search} ⇓', 'neosub'),
            InlineKeyboardButton(f'⌗ Iɴꜰᴏ', 'reqinfo')
        ]
    )
    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⇚ Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"〄 Pᴀɢᴇ {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"〄 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("Nᴇxᴛ​ ​⇛", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⇚ Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"〄 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ​ ​⇛", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)  #alrtxtincript
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)   #oldalrttxt in script
    movie = movies[(int(movie_))]
    temp_name = movie.replace(" ", "+")
    button = [[
        InlineKeyboardButton("♽ Mᴏᴠɪᴇ Rᴇᴏ̨ᴜᴇsᴛ Gʀᴏᴜᴘ ♽", url="t.me/+3sc743KKHWoxZDY1")
    ]]
    await query.message.edit(script.CHK_MOV_TXT)  #checkthemovie in db script
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            await query.message.delete()
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit(
                text=script.MVE_NT_FND,
                reply_markup=InlineKeyboardMarkup(button)
            ) 
            await asyncio.sleep(25)
            await k.delete()

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):    
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "gfiltersdeleteallconfirm":
        await del_allg(query.message, 'gfilters')
        await query.answer("Done !")
        return
    elif query.data == "gfiltersdeleteallcancel": 
        await query.message.reply_to_message.delete()
        await query.message.delete()
        await query.answer("Process Cancelled !")
        return
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('Piracy Is Crime')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        clicked = query.from_user.id
        try:
            typed = query.message.reply_to_message.from_user.id
        except:
            typed = clicked
        if typed != clicked:
            return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if (AUTH_CHANNEL or REQ_CHANNEL) and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                await query.answer('𝘾𝙝𝙚𝙘𝙠 𝙋𝙈, 𝙄 𝙝𝙖𝙫𝙚 𝙨𝙚𝙣𝙩 𝙛𝙞𝙡𝙚𝙨 𝙞𝙣 𝙥𝙢', show_alert=True)
                return
            else:
                if button_data in CLICK and CLICK[button_data] >= max_clicks:
                    await query.answer("okda 😋", show_alert=True)
                    return
                hack = await client.send_cached_media(
                    chat_id=FILE_CHANNEL,
                    file_id=file_id,
                    caption=script.CHANNEL_CAP.format(query.from_user.mention, title, query.message.chat.title),
                    protect_content=True if ident == "filep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔥 ᴄʜᴀɴɴᴇʟ 🔥", url=(MAIN_CHANNEL))
                            ]
                        ]
                    )
                )
                jr = await query.message.reply_text(
                    script.FILE_MSG.format(query.from_user.mention, title, size),
                    parse_mode=enums.ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup(
                        [
                         [
                          InlineKeyboardButton('📥 Rᴇᴏ̨ᴜᴇsᴛ Rᴇᴅɪʀᴇᴄᴛ Cʜᴀɴɴᴇʟ 📥 ', url = (FILE_FORWARD))
                       ],[
                          InlineKeyboardButton("⚠️ Nᴏᴡ Cʟɪᴄᴋ Hᴇʀᴇ Fᴏʀ Fɪʟᴇ 🥰 ⚠️", url=file_send.link)
                         ]
                        ]
                    )
                )
                CLICK[button_data] = CLICK.get(button_data, 0) + 1
                await asyncio.sleep(60)
                await jr.delete()
                await hack.delete()
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if (AUTH_CHANNEL or REQ_CHANNEL) and not await is_subscribed(client, query):
            await query.answer("I Lɪᴋᴇ Yᴏᴜʀ Sᴍᴀʀᴛɴᴇss, Bᴜᴛ Dᴏɴ'ᴛ Bᴇ Oᴠᴇʀsᴍᴀʀᴛ 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        msg = await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                  InlineKeyboardButton("♽ Mᴏᴠɪᴇ Rᴇᴏ̨ᴜᴇsᴛ Gʀᴏᴜᴘ ♽", url="t.me/+3sc743KKHWoxZDY1")
                 ]
                ]
            )
        ) 
        k = await msg.reply("<b><u>❗️❗️IMPORTANT❗️️❗️</u>\n\n⚠️ This File Will Be Deleted From Here Within <u>10 Minute</u>\n\nPlease Forward This File To Your Saved Messages And Start Download There ☺️.</b>",quote=True)
        await asyncio.sleep(50)
        await msg.delete()
        await k.delete()        
        return

    elif query.data == "whyjoin":
        await query.answer(text=script.WHYJOIN, show_alert=True)
    elif query.data == "neosub": 
        await query.answer(f"✯ താഴെയുള്ള ബട്ടണിൽ വേണ്ട ക്വാളിറ്റി യിൽ ക്ലിക്ക് ചെയ്താൽ കിട്ടും⚡\n\n✯ 𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 𝗙𝗶𝗹𝗲 𝗡𝗮𝗺𝗲 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇 𝖠𝗇𝖽 𝖲𝗍𝖺𝗋𝗍 𝖳𝗁𝖾 𝖡𝗈𝗍 🎯 \n\n➠ © @Team_KL",show_alert=True)
    elif query.data == "reqinfo":
        await query.answer("✯ Movies - Jailer 2023\n✯ Series - Dark S01E01\n\n✯ Correct Spelling in English Letters Only And ❌ Don't Use Stylish Font\n\n✯ Not Available Theater Print Files !\n\n ➠ © @Team_KL", show_alert=True)        
    elif query.data == "pages":
        await query.answer()

    elif query.data == "statx":
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - BOT_START_TIME))
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.answer(f"⚡️ Sʏsᴛᴇᴍ Sᴛᴀᴛᴜs ⚡️\n\n❂ Uᴘᴛɪᴍᴇ : {currentTime}\n✇ Cᴘᴜ : {cpu_usage}\n✪ Rᴀᴍ : {ram_usage}\n✼ Tᴏᴛᴀʟ Dɪsᴋ : {total}\n❐ Usᴇᴅ Sᴘᴀᴄᴇ : {used} ({disk_usage}%)\n❦ Fʀᴇᴇ Sᴘᴀᴄᴇ : {free}\n\nᴠ2.9.1 [sᴛᴀʙʟᴇ]", show_alert=True)
    
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('🎭 Bᴏᴛ Oᴡɴᴇʀ', callback_data="owner_info"),
            InlineKeyboardButton('🕵️ Sᴇᴀʀᴄʜ', switch_inline_query_current_chat='')            
            ],[      
            InlineKeyboardButton('✨ Hᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('🔮 Aʙᴏᴜᴛ', callback_data='about')
            ],[
            InlineKeyboardButton('🏮 Tᴇᴀᴍ Kʟ Oꜰꜰɪᴄɪᴀʟ Lɪɴᴋs 🏮', callback_data="group_info")
        ]]   
        reply_markup = InlineKeyboardMarkup(buttons)
        T = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        Time = T.hour        
        if Time < 12:
            afsu="Gᴏᴏᴅ Mᴏʀɴɪɴɢ" 
        elif Time < 15:
            afsu="Gᴏᴏᴅ AғᴛᴇʀNᴏᴏɴ" 
        elif Time < 20:
            afsu="Gᴏᴏᴅ Eᴠᴇɴɪɴɢ"
        else:
            afsu="Gᴏᴏᴅ Nɪɢʜᴛ"
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(afsu, query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Fɪʟᴛᴇʀ', callback_data='filters'),     
            InlineKeyboardButton('Fɪʟᴇ Sᴛᴏʀᴇ', callback_data='store_file')
        ], [
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴꜱ', callback_data='coct'),
            InlineKeyboardButton('Exᴛʀᴀ Mᴏᴅꜱ', callback_data='extra')                        
        ], [
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='start'),
            InlineKeyboardButton('〄 Sᴛᴀᴛᴜs', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )            
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('ᠰ Sᴇʀᴠᴇʀ Iɴꜰᴏ', callback_data='statx'),
            InlineKeyboardButton('✇ Sᴏᴜʀᴄᴇ', callback_data='source')
        ], [
            InlineKeyboardButton('⇍ Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('⌬ ᥴꪶꪮꪀꫀ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "filters":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴇʟ Fɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ', callback_data='autofilter')            
        ], [
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Gʟᴏʙᴀʟ Fɪʟᴛᴇʀ', callback_data='gfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FIlTERS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )   
    elif query.data == "gfilter":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='filters')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(text=script.GLOBE_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        else:
            await query.answer("🤔 Tʜɪɴᴋ Yᴏᴜ. Aʀᴇ Yᴏᴜ Nᴏᴛ Mʏ Aᴅᴍɪɴ..? Sᴏ Tʜɪꜱ Cᴏᴍᴍᴇɴᴛ Iꜱ Nᴏᴛ Fᴏʀ Yᴏᴜ 🤗", show_alert=True)                        
    elif query.data == "store_file":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FILE_STORE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )    
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ Tᴏ Aʙᴏᴜᴛ ⇏', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://telegra.ph/file/e753f50b93fb047d1f551.jpg")
        )
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='filters'),
            InlineKeyboardButton('⍞ Bᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='filters')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "owner_info":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='start'),
            InlineKeyboardButton ('𓄀 ᥴꫝꪖꪀꪀꫀꪶ', url="t.me/PremiumLogoPro")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://telegra.ph/file/9a790ac02f21aa343e3d3.jpg")
        )
        await query.message.edit_text(
            text=script.OWNER_INFO,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )       
    elif query.data == "group_info":
        buttons = [[
            InlineKeyboardButton("⟁ Sᴜʙsᴄʀɪʙᴇ Yᴏᴜᴛᴜʙᴇ Cʜᴀɴɴᴇʟ ⟁", url="https://youtube.com/shorts/v66wWBXzVYY?si=s5hpGq5p1jCFe6fR")         
                  ],[
            InlineKeyboardButton("• Tᴇᴀᴍ Kʟ Mᴀɪɴ Cʜᴀɴɴᴇʟ •", url="t.me/team_kl")
                  ],[
            InlineKeyboardButton("• Gʀᴏᴜᴘ 1 •", url="https://t.me/KLMovieGroup"),
            InlineKeyboardButton("• Gʀᴏᴜᴘ 2 •", url="https://t.me/KL_Group2")
                  ],[           
            InlineKeyboardButton("• കേരള റോക്കേഴ്സ് [Nᴇᴡ Gʀᴏᴜᴘ] •", url="https://t.me/+3sc743KKHWoxZDY1")
                  ],[
            InlineKeyboardButton("⇍ Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ ⇏", callback_data="start")
        ]]   
        reply_markup = InlineKeyboardMarkup(buttons)        
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/ee19a2739a0a082b0ca9a.jpg")
        )
        await query.message.edit_text(
            text=script.GROUP_INFO,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )            
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⛯ ​ꪖᦔꪑ𝓲ꪀ', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(text=script.ADMIN_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        else:
            await query.answer("🤔 Tʜɪɴᴋ Yᴏᴜ. Aʀᴇ Yᴏᴜ Nᴏᴛ Mʏ Aᴅᴍɪɴ..? Sᴏ Tʜɪꜱ Cᴏᴍᴍᴇɴᴛ Iꜱ Nᴏᴛ Fᴏʀ Yᴏᴜ 🤗", show_alert=True)        
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('↺ 𝘳ꫀᠻ𝘳ꫀ𝘴ꫝ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("𝐹𝐸𝑇𝐶𝐻𝐼𝑁𝐺 𝑀𝑂𝑁𝐺𝑂𝐷𝐵 𝐷𝐴𝑇𝐴𝐵𝐴𝑆𝐸𝑆")
        buttons = [[
            InlineKeyboardButton('⇍ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('↺ 𝘳ꫀᠻ𝘳ꫀ𝘴ꫝ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if set_type == 'botpm' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)

        if set_type == 'button' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)

        if set_type == 'welcome' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)
        
        if set_type == 'file_secure' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)

        if set_type == 'imdb' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)

        if set_type == 'spell_check' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)
        
        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)
        try:
            if settings['auto_delete']:
                settings = await get_settings(grp_id)
        except KeyError:
            await save_group_settings(grp_id, 'auto_delete', True)
            settings = await get_settings(grp_id)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],              
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer('⏤͟͟͞ ♡ Nᴀɴᴄʏ ᵛ³·⁰ 🦄')


async def auto_filter(client, msg, spoll=False):
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(client, msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"★ {get_size(file.file_size)} ⊳ {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
            ]
            for file in files
        ]
    btn.insert(0, 
        [
            InlineKeyboardButton(f"⇓ {search} ⇓", "neosub"),
            InlineKeyboardButton(f"⌗ Iɴꜰᴏ", "reqinfo")       
        ]
    )
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"〄 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="Nᴇxᴛ​ ​⇛", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="〄 1/1 〄", callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>┏⍞ Tɪᴛɪʟᴇ : {search}\n┣❐ Asᴋᴇᴅ Bʏ : {message.from_user.mention}\n┣⎙ Fɪʟᴇs : [{total_results}](tg://need_update_for_some_feature)\n┗〄 Pᴏᴡᴇʀᴇᴅ Bʏ : [kᴇʀᴀʟᴀ Rᴏᴄᴋᴇʀs](https://t.me/Team_KL)</b>"
    if imdb and imdb.get('poster'):
        try:
            fmsg = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            fmsg = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            fmsg = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        fmsg = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(55)
    await fmsg.delete()
    await message.delete()
    if spoll:
        await msg.message.delete()

async def advantage_spell_chok(client, msg):
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    try:
        movies = await get_poster(mv_rqst, bulk=True)
    except Exception as e:
        logger.exception(e)
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
        InlineKeyboardButton('⌬ ᧁꪮꪮᧁꪶꫀ ⌬', url=f'https://google.com/search?q={reqst_gle}'),
        InlineKeyboardButton('✽ 𝓲ꪑᦔ᥇ ✽', url=f'https://www.imdb.com/find/?q={reqst_gle}&ref_=nv_sr_sm')
        ]]
        k = await msg.reply_photo(
            photo=SPELL_IMG, 
            caption=script.SPEL_CHK.format(mv_rqst),
            reply_markup=InlineKeyboardMarkup(button),
            reply_to_message_id=msg.id
        )
        await asyncio.sleep(35)
        await msg.delete()
        await k.delete()      
        return
    movielist = []
    if not movies:
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
        InlineKeyboardButton('⌬ ᧁꪮꪮᧁꪶꫀ ⌬', url=f'https://google.com/search?q={reqst_gle}'),
        InlineKeyboardButton('✽ 𝓲ꪑᦔ᥇ ✽', url=f'https://www.imdb.com/find/?q={reqst_gle}&ref_=nv_sr_sm')
        ]]
        k = await msg.reply_photo(
            photo=SPELL_IMG, 
            caption=script.SPEL_CHK.format(mv_rqst),
            reply_markup=InlineKeyboardMarkup(button),
            reply_to_message_id=msg.id
        )
        await asyncio.sleep(35)
        await msg.delete()
        await k.delete()
        return
    movielist = [movie.get('title') for movie in movies]
    SPELL_CHECK[mv_id] = movielist
    btn = [
        [
            InlineKeyboardButton(
                text=f"◉ {movie_name.strip()}",
                callback_data=f"spol#{reqstr1}#{k}",
            )
        ]
        for k, movie_name in enumerate(movielist)
    ]
    btn.append([InlineKeyboardButton(text="✘ ᴄʟᴏsᴇ ✘", callback_data=f'spol#{reqstr1}#close_spellcheck')])
    spell_check_del = await msg.reply_text(
        text=(script.CUDNT_FND.format(mv_rqst)),
        reply_markup=InlineKeyboardMarkup(btn),
        reply_to_message_id=msg.id
    )
    await asyncio.sleep(25)
    await spell_check_del.delete()
    await msg.delete()

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            kk = await client.send_message(
                                group_id,
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(40)
                            await kk.delete()
                            await message.delete()
                        else:
                            button = eval(btn)
                            grg = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(40)
                            await grg.delete()
                            await message.delete()
                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(40)
                        await joelkb.delete()
                        await message.delete()
                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(40)
                        await dlt.delete()
                        await message.delete()
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def global_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(40)
                            await joelkb.delete()
                            await message.delete()
                            
                        else:
                            button = eval(btn)
                            hmm = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(40)
                            await hmm.delete()
                            await message.delete()

                    elif btn == "[]":
                        oto = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(40)
                        await oto.delete()
                        await message.delete()

                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(40)
                        await dlt.delete()
                        await message.delete()
 
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
