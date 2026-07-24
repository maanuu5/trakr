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

## How to Run (Beginner's Guide)

If you are running this project from scratch, follow these step-by-step instructions.

### 1. Prerequisites
Before starting, you must have the following installed on your machine:
- **Docker Desktop:** Required to run SigNoz locally. [Download and install it here.](https://www.docker.com/products/docker-desktop/) Make sure to allocate at least 4GB of RAM in Docker settings.
- **Foundry:** The CLI tool used to deploy SigNoz. [Install it here.](https://github.com/WeMakeDevs/foundry)
- **Python:** Required to run the observer bot. [Download Python 3.10+ here.](https://www.python.org/downloads/)
- **Git:** Required to clone this repository. [Download Git here.](https://git-scm.com/downloads)

### 2. Set Up a Discord Bot
The observer needs a Discord bot token to connect to your server and read events.
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** in the top right, name it (e.g., "Trakr"), and accept the terms.
3. On the left sidebar, click **Bot**.
4. Scroll down to **Privileged Gateway Intents** and enable:
   - **Presence Intent**
   - **Server Members Intent**
   *(Save your changes at the bottom).*
5. Scroll back up to the **Token** section and click **Reset Token**. Copy the token that appears. Keep this secret!
6. On the left sidebar, click **OAuth2** → **URL Generator**.
7. Under "Scopes", select `bot`.
8. Under "Bot Permissions", select `View Channels`, `Read Message History`, and `View Audit Log`.
9. Copy the generated URL at the bottom, paste it into your browser, and invite the bot to your test server.

### 3. Deploy SigNoz
1. Open a terminal (Command Prompt, PowerShell, or macOS Terminal).
2. Clone this repository and move into it:
   ```bash
   git clone https://github.com/maanuu5/trakr.git
   cd trakr
   ```
3. Ensure Docker Desktop is running, then deploy SigNoz using Foundry:
   ```bash
   foundryctl cast -f casting.yaml
   ```
4. Wait a few minutes for the containers to spin up. Open `http://localhost:8080` in your web browser. If you see the SigNoz login screen, it worked! (Create an admin account to log in).

### 4. Start the Trakr Observer
1. Navigate into the `observer` directory:
   ```bash
   cd observer
   ```
2. Create a configuration file named `.env` in this directory (exactly `.env`, no filename before the dot) and add your Discord token:
   ```env
   DISCORD_TOKEN=your_token_from_step_2
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the bot!
   ```bash
   python bot.py
   ```
   *You should see logs indicating the bot has connected to Discord and initialized OpenTelemetry.*

### 5. Import the Dashboards
Now that data is flowing, you need to set up the graphs in SigNoz.
1. Go to your SigNoz dashboard at `http://localhost:8080`.
2. On the left sidebar, click **Dashboards**.
3. In the top right, click **New Dashboard** → **Import JSON**.
4. Navigate to the `trakr/dashboards/` folder on your computer.
5. Upload all four JSON files (`bot_activity.json`, `moderation_actions.json`, `recovery_funnel.json`, `uptime_reliability.json`).
6. Click into any of them to see your real-time Discord server telemetry!

## Dashboards

1. **Bot Uptime & Reliability:** Displays uptime percentages and crash events.
2. **Bot Activity:** Shows message volume broken down by bot.
3. **Moderation Actions:** Visualizes automated moderation events over time.
4. **Recovery Funnel:** Tracks the progression from a crash to a successful recovery and the first message sent.

## Notice

This project was built for a hackathon. The Python observer script, OpenTelemetry configuration, and SigNoz queries were developed with the assistance of an AI coding agent. All architecture decisions and final implementations were reviewed and deployed by the developer.
