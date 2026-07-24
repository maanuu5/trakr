# Trakr

Trakr is a monitoring tool for Discord servers that use multiple bots. It provides a single dashboard for bot activity, uptime, and moderation actions, allowing administrators to verify that their automated systems are online and functioning correctly.

## Features

- **Uptime Monitoring:** Tracks which bots are online and records periods of downtime.
- **Activity Tracking:** Monitors message volume across all bots to measure usage and identify unresponsive bots.
- **Moderation Audit:** Logs timeouts, kicks, and bans performed by bots to help audit automated moderation rules.
- **Recovery Tracking:** Cross-references downtime events with subsequent message activity to confirm when a bot has fully recovered from a crash.
- **Alerting:** Triggers notifications for bot crashes, abnormal drops in activity, or telemetry pipeline failures.

## Architecture

Trakr uses a Python observer script that polls the Discord API for presence data, message events, and audit logs. It formats this data into OpenTelemetry metrics and exports them to SigNoz for visualization and alerting.

- **Backend:** Python, discord.py
- **Telemetry:** OpenTelemetry SDK
- **Observability:** SigNoz
- **Storage:** SQLite (local state management for audit logs)

## Dashboards

1. **Bot Uptime & Reliability:** Displays uptime percentages and crash events.
2. **Bot Activity:** Shows message volume broken down by bot.
3. **Moderation Actions:** Visualizes automated moderation events over time.
4. **Recovery Funnel:** Tracks the progression from a crash to a successful recovery and the first message sent.

## Notice

This project was built for a hackathon. The Python observer script, OpenTelemetry configuration, and SigNoz queries were developed with the assistance of an AI coding agent. All architecture decisions and final implementations were reviewed and deployed by the developer.
