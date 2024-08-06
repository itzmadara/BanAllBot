import logging
import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChannelParticipantsKicked
from telethon.errors.rpcerrorlist import FloodWaitError

RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

logging.basicConfig(level=logging.INFO)

print("Starting.....")

Riz = TelegramClient('Riz', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)

SUDO_USERS = []
for x in Var.SUDO: 
    SUDO_USERS.append(x)

@Riz.on(events.NewMessage(pattern="^/ping"))
async def ping(event):
    if event.sender_id in SUDO_USERS:
        start = datetime.now()
        text = "Pong!"
        event_msg = await event.reply(text, parse_mode=None, link_preview=None)
        end = datetime.now()
        ms = (end-start).microseconds / 1000
        await event_msg.edit(f"**I'm On** \n\n __Pong__ !! `{ms}` ms")

@Riz.on(events.NewMessage(pattern="^/banall"))
async def banall(event):
    if event.sender_id in SUDO_USERS:
        if not event.is_channel:
            Reply = "Noob !! Use This Cmd in a Channel."
            await event.reply(Reply)
        else:
            await event.delete()
            channel = await event.get_chat()
            admin = channel.admin_rights
            creator = channel.creator
            if not admin and not creator:
                return await event.reply("I Don't have sufficient Rights !!")
            RiZoeL = await Riz.send_message(event.chat_id, "**Hello !! I'm Alive**")
            admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
            admins_id = [i.id for i in admins]
            all = 0
            bann = 0
            async for user in event.client.iter_participants(event.chat_id):
                all += 1
                try:
                    if user.id not in admins_id:
                        await event.client(functions.channels.EditBannedRequest(event.chat_id, user.id, RIGHTS))
                        bann += 1
                        await asyncio.sleep(0.1)
                except Exception as e:
                    print(str(e))
                    await asyncio.sleep(0.1)
            await RiZoeL.edit(f"**Users Banned Successfully! \n\n Banned Users:** `{bann}` \n **Total Users:** `{all}`")

@Riz.on(events.NewMessage(pattern="^/unbanall"))
async def unban(event):
    if event.sender_id in SUDO_USERS:
        if not event.is_channel:
            Reply = "Noob !! Use This Cmd in a Channel."
            await event.reply(Reply)
        else:
            msg = await event.reply("Searching Participant Lists.")
            p = 0
            async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
                rights = ChatBannedRights(until_date=0, view_messages=False)
                try:
                    await event.client(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                except FloodWaitError as ex:
                    print(f"sleeping for {ex.seconds} seconds")
                    await asyncio.sleep(ex.seconds)
                except Exception as ex:
                    await msg.edit(str(ex))
                else:
                    p += 1
            await msg.edit("{}: {} unbanned".format(event.chat_id, p))

@Riz.on(events.NewMessage(pattern="^/leave"))
async def leave(event):
    if event.sender_id in SUDO_USERS:
        if len(event.text.split()) > 1:
            bc = int(event.text.split()[1])
            text = "Leaving....."
            event_msg = await event.reply(text, parse_mode=None, link_preview=None)
            try:
                await event.client(LeaveChannelRequest(bc))
                await event_msg.edit("Successfully Left")
            except Exception as e:
                await event_msg.edit(str(e))
        else:
            bc = event.chat_id
            text = "Leaving....."
            event_msg = await event.reply(text, parse_mode=None, link_preview=None)
            try:
                await event.client(LeaveChannelRequest(bc))
                await event_msg.edit("Successfully Left")
            except Exception as e:
                await event_msg.edit(str(e))

@Riz.on(events.NewMessage(pattern="^/restart"))
async def restart(event):
    if event.sender_id in SUDO_USERS:
        text = "__Restarting__ !!!"
        await event.reply(text, parse_mode=None, link_preview=None)
        try:
            await Riz.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()

print("\n\n")
print("Your Ban All Bot Deployed Successfully ✅")

Riz.run_until_disconnected()
