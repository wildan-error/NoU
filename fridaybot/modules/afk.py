"""AFK Plugin for @FridayOT
Syntax: .afk REASON"""
import asyncio
import datetime
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from fridaybot import CMD_HELP

global USER_AFK
global afk_time
global last_afk_message
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@friday.on(
    events.NewMessage(pattern=r"\.afk ?(.*)", outgoing=True)
)
async def _(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    if not USER_AFK:
        last_seen_status = await borg(  
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()
        USER_AFK = f"yes: {reason}"
        if reason:
            await borg.send_message(
                event.chat_id,
                f"**he's ded again ffs, can someone wake him up?** \n__He is ded Because Of__ `{reason}`",
            )
        else:
            await borg.send_message(event.chat_id, f"**ded right now. come back later when resurrected**.")
        await asyncio.sleep(5)
        await event.delete()
        try:
            await borg.send_message(
                Config.PRIVATE_GROUP_ID,
                f"#AfkLogger Afk Is Active And Reason is {reason}",
            )
        except Exception as e:
            logger.warn(str(e))


@friday.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
async def set_not_afk(event):
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if ".afk" not in current_message and "yes" in USER_AFK:
        shite = await borg.send_message(
            event.chat_id,
            "__RESURRECTED!__\n**No Longer ded.**\n `I Was ded for:``"
            + total_afk_time
            + "`",
        )
        try:
            await borg.send_message(
                Config.PRIVATE_GROUP_ID,
                "#AfkLogger User is Back Alive ! No Longer ded ",
            )
        except Exception as e:
            await borg.send_message(
                event.chat_id,
                "Please set `PRIVATE_GROUP_ID` "
                + "for the proper functioning of afk functionality "
                + "Please Seek Support in @FridayOT\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True,
            )
        await asyncio.sleep(5)
        await shite.delete()
        USER_AFK = {}
        afk_time = None


@friday.on(
    events.NewMessage(
        incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
    )
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    afk_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # fridaybot's should not reply to other fridaybot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFK and not (await event.get_sender()).bot:
        if afk_time:
            now = datetime.datetime.now()
            datime_since_afk = now - afk_time
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    wday.strftime("%A")
            elif hours > 1:
                f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                f"`{int(seconds)}s` **ago**"
        msg = None
        message_to_reply = (f"I Am **[AFK]** Right Now. \n**Last Seen :** `{total_afk_time}`\n**Reason** : `{reason}`" if reason else f"I Am **[AFK]** Right Now. \n**Last Seen :** `{total_afk_time}`")
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg


CMD_HELP.update(
    {
        "afk": ".afk <Reason> \
\nUsage: Gets You Afk"
    }
)
