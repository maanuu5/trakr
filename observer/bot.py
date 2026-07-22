import os
import discord
from otel import init_otel
import store
import audit_poll

# -----------------------------
# OpenTelemetry Setup
# -----------------------------
meter, logger = init_otel()

bot_online_gauge = meter.create_gauge("trakr.bot.online")
message_counter = meter.create_counter("trakr.bot.messages")
downtime_histogram = meter.create_histogram("trakr.bot.downtime_seconds", unit="s")

# -----------------------------
# Discord Setup
# -----------------------------
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f"Connected as {client.user} — watching {len(client.guilds)} server(s)")
    print(f"Connected as {client.user} — watching {len(client.guilds)} server(s)")
    if not poll_task.is_running():
        poll_task.start()

@client.event
async def on_presence_update(before, after):
    try:
        if not after.bot:
            return

        if before.status == after.status:
            return

        is_online = 1 if str(after.status) != "offline" else 0
        bot_id = str(after.id)
        attrs = {
            "bot.name": after.name,
            "bot.id": bot_id,
        }
        
        bot_online_gauge.set(is_online, attrs)
        
        # State Tracking
        if is_online == 0:
            store.mark_offline(bot_id)
        else:
            downtime = store.mark_online(bot_id)
            if downtime is not None:
                downtime_histogram.record(downtime, attrs)
                logger.info(f"{after.name} recovered after {downtime:.1f}s downtime", extra=attrs)
                print(f"[recovery] {after.name} recovered after {downtime:.1f}s")
        
        log_msg = f"{after.name} went {after.status}"
        logger.info(log_msg, extra=attrs)
        print(f"[presence] {log_msg}")

    except Exception as e:
        logger.exception("Error in on_presence_update")

@client.event
async def on_message(message):
    try:
        if not message.author.bot:
            return

        if message.author.id == client.user.id:
            return

        attrs = {
            "bot.name": message.author.name,
            "bot.id": str(message.author.id),
            "channel": str(message.channel),
        }
        
        message_counter.add(1, attrs)
        
        log_msg = f"{message.author.name} posted in #{message.channel}"
        logger.info(log_msg, extra=attrs)
        print(f"[message] {log_msg}")

    except Exception as e:
        logger.exception("Error in on_message")

@client.event
async def on_member_remove(member):
    try:
        if not member.bot:
            return
            
        bot_id = str(member.id)
        store.mark_offline(bot_id)
        
        attrs = {
            "bot.name": member.name,
            "bot.id": bot_id,
        }
        bot_online_gauge.set(0, attrs)
        
        log_msg = f"{member.name} left the server (marked as offline)"
        logger.info(log_msg, extra=attrs)
        print(f"[presence] {log_msg}")
    
    except Exception as e:
        logger.exception("Error in on_member_remove")

@client.event
async def on_member_join(member):
    try:
        if not member.bot:
            return
        
        bot_id = str(member.id)
        downtime = store.mark_online(bot_id)
        
        attrs = {
            "bot.name": member.name,
            "bot.id": bot_id,
        }
        bot_online_gauge.set(1, attrs)
        
        if downtime is not None:
            downtime_histogram.record(downtime, attrs)
            log_msg = f"{member.name} re-joined after {downtime:.1f}s absence"
            logger.info(log_msg, extra=attrs)
            print(f"[recovery] {log_msg}")
        else:
            log_msg = f"{member.name} joined the server"
            logger.info(log_msg, extra=attrs)
            print(f"[presence] {log_msg}")
    
    except Exception as e:
        logger.exception("Error in on_member_join")

# -----------------------------
# Background Tasks
# -----------------------------
poll_task = audit_poll.setup_audit_poll(client, meter, logger)

# -----------------------------
# Start Bot
# -----------------------------
token = os.environ.get("DISCORD_BOT_TOKEN")

if not token:
    raise SystemExit(
        "DISCORD_BOT_TOKEN is not set.\n\n"
        "PowerShell:\n"
        '$env:DISCORD_BOT_TOKEN="YOUR_TOKEN_HERE"'
    )

client.run(token)