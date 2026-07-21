import os
import discord
from otel import init_otel

# -----------------------------
# OpenTelemetry Setup
# -----------------------------
meter, logger = init_otel()

bot_online_gauge = meter.create_gauge("trakr.bot.online")
message_counter = meter.create_counter("trakr.bot.messages")

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

@client.event
async def on_presence_update(before, after):
    try:
        if not after.bot:
            return

        if before.status == after.status:
            return

        is_online = 1 if str(after.status) != "offline" else 0
        attrs = {
            "bot.name": after.name,
            "bot.id": str(after.id),
        }
        
        bot_online_gauge.set(is_online, attrs)
        
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