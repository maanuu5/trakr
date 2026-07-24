# Absent-Data Alert (Observer Down)

- **Metric:** `trakr.bot.online` (Count, no grouping)
- **Condition:** BELOW -1 (to intentionally disable the standard threshold)
- **Advanced Options:** "Alert when data stops coming" toggled **ON** for **15 Minutes**.
- **Purpose:** Alerts if the Python observer script crashes or the telemetry pipeline completely fails, resulting in 15 straight minutes of zero data points received.
