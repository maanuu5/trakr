import os
import discord

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

# -----------------------------
# OpenTelemetry -> SigNoz Setup
# -----------------------------

resource = Resource.create(
    {
        "service.name": "trakr"
    }
)

exporter = OTLPMetricExporter(
    endpoint="localhost:4317",
    insecure=True,
)

reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5000,
)

metrics.set_meter_provider(
    MeterProvider(
        resource=resource,
        metric_readers=[reader],
    )
)

meter = metrics.get_meter("trakr")

# Day 1 metrics
presence_counter = meter.create_counter("trakr.presence_changes")
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
    print(
        f"Connected as {client.user} — watching {len(client.guilds)} server(s)"
    )


@client.event
async def on_presence_update(before, after):
    if not after.bot:
        return

    if before.status == after.status:
        return

    presence_counter.add(
        1,
        {
            "bot.name": after.name,
            "new_status": str(after.status),
        },
    )

    print(f"[presence] {after.name} -> {after.status}")


@client.event
async def on_message(message):
    if not message.author.bot:
        return

    if message.author.id == client.user.id:
        return

    message_counter.add(
        1,
        {
            "bot.name": message.author.name,
        },
    )

    print(
        f"[message] {message.author.name} posted in #{message.channel}"
    )


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