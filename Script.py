class script(object):
    START_TXT = """<b>{} {},

Mʏ Nᴀᴍᴇ Is <a href=https://t.me/{}>{}</a>, Yᴏᴜ Cᴀɴ Usᴇ Mᴇ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ I Wɪʟʟ Gɪᴠᴇ Mᴏᴠɪᴇs Oʀ Sᴇʀɪᴇs Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Pᴍ.</b>"""   

    HELP_TXT = """<b>Hᴇʏ {} Hᴇʀᴇ Is Tʜᴇ Hᴇʟᴘ Fᴏʀ Mʏ Cᴏᴍᴍᴀɴᴅs.</b>"""

    ABOUT_TXT = """<b>◆ Mʏ Nᴀᴍᴇ : <a href='https://t.me/Oru_adaar_Robot'>♡ Nᴀɴᴄʏ ᵛ³·⁰</a>
◆ Dᴇᴠᴇʟᴏᴘᴇʀ: <a href='https://t.me/Hacker_Jr'>HᴀᴄKᴇʀ Jʀ 〆⁪⁬⁮⁮⁮</a>
◆ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʀᴏɢʀᴀᴍ</a>
◆ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/'>Pʏᴛʜᴏɴ 3</a>
◆ Dᴀᴛᴀ Bᴀsᴇ: <a href='https://cloud.mongodb.com/'>Mᴏɴɢᴏ Dʙ</a>
◆ Bᴏᴛ Sᴇʀᴠᴇʀ: <a href='https://railway.app/'>Rᴀɪʟᴡᴀʏ</a>
◆ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: v2.7.1 [ Sᴛᴀʙʟᴇ ]</b>"""

    SOURCE_TXT = """<b>
⚠️ Tʜɪꜱ Bᴏᴛ Iꜱ Aɴ Oᴘᴇɴ Sᴏᴜʀᴄᴇ Pʀᴏᴊᴇᴄᴛ ⚠️

◆ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ : <a href='https://github.com/EvamariaTG/EvaMaria'>Cʟɪᴄᴋ Hᴇʀᴇ</a>  

◆ Aʟʟ Cʀᴇᴅɪᴛs​: <a href='https://t.me/TeamEvamaria'>Team Eva Maria</a></b>"""

    MANUELFILTER_TXT = """<b><u>FILTERS COMMANDS</u></b>

• /filter - <code>add a filter in chat</code>
• /filters - <code>list all the filters of a chat</code>
• /del - <code>delete a specific filter in chat</code>
• /delall - <code>delete the whole filters in a chat (chat owner only)</code>"""

    BUTTON_TXT = """<b><u>BUTTONS NOTE:-</u></b>

• ᴛᴇʟᴇɢʀᴀᴍ ᴡɪʟʟ ɴᴏᴛ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ sᴇɴᴅ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴄᴏɴᴛᴇɴᴛ, sᴏ ᴄᴏɴᴛᴇɴᴛ ɪs ᴍᴀɴᴅᴀᴛᴏʀʏ.
• ɴᴀɴᴄʏ ʙᴏᴛ sᴜᴘᴘᴏʀᴛs ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.
• ʙᴜᴛᴛᴏɴs sʜᴏᴜʟᴅ ʙᴇ ᴘʀᴏᴘᴇʀʟʏ ᴘᴀʀsᴇᴅ ᴀs ᴍᴀʀᴋᴅᴏᴡɴ ꜰᴏʀᴍᴀᴛ.

<b><u>URL BUTTONS:-</u></b>
<code>[Button Text](buttonurl:https://t.me/Oru_adaar_Robot)</code>

<b><u>ALERT BUTTONS:-</u></b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""

    AUTOFILTER_TXT = """<b><u>AUTO FILTER NOTE:-</u></b>

• ᴍᴀᴋᴇ ᴍᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏꜰ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ɪꜰ ɪᴛ's ᴘʀɪᴠᴀᴛᴇ.
• ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴs ᴄᴀᴍʀɪᴘs, ᴘᴏʀɴ ᴀɴᴅ ꜰᴀᴋᴇ ꜰɪʟᴇs.
• ꜰᴏʀᴡᴀʀᴅ ᴛʜᴇ ʟᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴇ ᴡɪᴛʜ ǫᴜᴏᴛᴇs. ɪ'ʟʟ ᴀᴅᴅ ᴀʟʟ ᴛʜᴇ ꜰɪʟᴇs ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴍʏ ᴅʙ."""

    CONNECTION_TXT = """<b><u>CONNECTIONS NOTE:-</u></b>

1. ONLY ADMINS CAN ADD A CONNECTION.
2. SEND <code>/connect</code> FOR CONNECTING ME TO UR PM

<b><u>COMMANDS AND USAGE:-</u></b>
• /connect  - <code>connect a particular chat to your PM</code>
• /disconnect  - <code>disconnect from a chat</code>
• /connections - <code>list all your connections</code>"""

    IMDB_TEMPLATE_TXT = """
<b>⍞ TɪᴛLᴇ : {title}
⌬ YᴇAʀ : {year}
✇ LᴀNɢUᴀGᴇ : {languages}
⛦ RᴀTɪNɢ : {rating} / 10.0
〄 QᴜAʟIᴛY : HDRip</b>"""
   
    CUSTOM_FILE_CAPTION = """<b>⋟ Fɪʟᴇ Nᴀᴍᴇ :- {file_name}

⋟ Fɪʟᴇ Sɪᴢᴇ :- {file_size}

⋟ @KLMovieGroup       
⋟ @KL_Group2</b>"""

    FILE_MSG = """
<b>Hai 👋 {} </b>😍

<b>📫 Your File is Ready</b>

<b>📂 Fɪʟᴇ Nᴀᴍᴇ</b> : <code>{}</code>              
                       
<b>⚙️ Fɪʟᴇ Sɪᴢᴇ</b> : <b>{}</b>
"""

    CHANNEL_CAP = """
<b>Hai 👋 {}</b> 😍

<code>{}</code>

⚠️ <b>This file will be deleted from here within 10 minute as it has copyright ... !!!</b>

<b>കോപ്പിറൈറ്റ് ഉള്ളതുകൊണ്ട് ഫയൽ 10 മിനിറ്റിനുള്ളിൽ ഇവിടെനിന്നും ഡിലീറ്റ് ആകുന്നതാണ് അതുകൊണ്ട് ഇവിടെ നിന്നും മറ്റെവിടെക്കെങ്കിലും മാറ്റിയതിന് ശേഷം ഡൗൺലോഡ് ചെയ്യുക!</b>

<b>© Powered by @Team_KL</b>
"""
    OWNER_INFO = """
<b>⍟───[ Oᴡɴᴇʀ Dᴇᴛᴀɪʟꜱ ]───⍟
    
• Fᴜʟʟ Nᴀᴍᴇ : • HᴀᴄKᴇʀ Jʀ ~ 🕊 
• Uꜱᴇʀɴᴀᴍᴇ : @Hacker_Jr
• Lᴏɢᴏ Mᴀᴋᴇʀ Cʜᴀɴɴᴇʟ : <a href='t.me/PremiumlogoPro'>Pʀᴇᴍɪᴜᴍ Lᴏɢᴏ Pʀᴏ 🃏</a></b>"""

    GROUP_INFO = """
<b>⍟ Wᴇʟᴄᴏᴍᴇ Tᴏ Tᴇᴀᴍ Kʟ Lɪɴᴋs ⍟</b>"""

    I_CUDNT = """ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴍᴏᴠɪᴇ ɪɴ ᴛʜᴀᴛ ɴᴀᴍᴇ"""

    WHYJOIN = """Iғ Tʜᴇ Gʀᴏᴜᴘ Cᴏᴘʏ Rɪɢʜᴛ Iꜱ Lᴏꜱᴛ, Wʜᴇɴ A Nᴇᴡ Gʀᴏᴜᴘ Iꜱ Sᴛᴀʀᴛᴇᴅ, Iᴛ Wɪʟʟ Bᴇ Nᴏᴛɪғɪᴇᴅ Oɴ Tʜɪꜱ Cʜᴀɴɴᴇʟ 🤥

© @Team_KL"""

    EXTRAMOD_TXT = """<b><u>EXTRA MODULES COMMANDS</u></b>

• /id - <code>get id of a specified user.</code>
• /info  - <code>get information about a user.</code>
• /imdb  - <code>get the film information from IMDb source.</code>
• /search  - <code>get the film information from various sources.</code>"""

    ADMIN_TXT = """<b><u>ADMIN MODS COMMANDS</u></b>

• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""

    STATUS_TXT = """<b>⍟───[ Sᴛᴀᴛᴜs Dᴇᴛᴀɪʟꜱ ]───⍟
    
⎇ Fɪʟᴇs Sᴀᴠᴇᴅ: <code>{}</code>
⎇ Tᴏᴛᴀʟ Usᴇʀs: <code>{}</code>
⎇ Tᴏᴛᴀʟ Cʜᴀᴛs: <code>{}</code>
⎇ Usᴇᴅ Sᴛᴏʀᴀɢᴇ: <code>{}</code> Mɪʙ
⎇ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ: <code>{}</code> Mɪʙ</b>"""

    ALRT_TXT = """Hello {},
This is Not your Request
Request Yourself...!!"""

    OLD_ALRT_TXT = """Hey {},
You are using one of old message,
Request Again"""

    CHK_MOV_TXT = """<b>Sᴇᴀʀᴄʜɪɴɢ Rᴇꜱᴜʟᴛꜱ. 🥴</b>"""

    SPEL_CHK = """<b>🥺 Sorry No File Found <u>{}</u>

▫️Use The Button Below To Search On <u>Google</u> Or <u>IMDB</u> And Copy The Correct Movie Name And Paste..!!

▪️Don't Ask Movies That Are Not Released In OTT Platform..!!

▪️Try To Ask In [Moviename, Year, Language] This Format..!! 

🚯 Don't Use: ➠ ':(!,./) 🙅‍♂</b>"""
    
    MVE_NT_FND = """<b>This Movie Not Available 😢

🤠 <u>For Reasons</u> 👀

◉) OTT Or DVD Not Released..!
◉) Type Name With Year..!
◉) check your correct spelling..!
◉) Movie Is Not Available in My Database..!
◉) Not Available Theater Print 🥴..!</b>"""
       
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}"""
