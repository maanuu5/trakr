# Anomaly Alert (Quiet Bot)
- **Metric:** `trakr.bot.messages` (Rate by bot.name)
- **Condition:** BELOW 0.01, ALL THE TIME, during the Last 10 minutes
- **Purpose:** Alerts when a bot's message rate drops significantly, acting as an anomaly detection for a bot that is online but broken/unresponsive.
