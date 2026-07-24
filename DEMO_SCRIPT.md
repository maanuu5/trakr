# Trakr: Hackathon Demo Script

*This script is designed for a 2-3 minute recorded video presentation for the hackathon judges.*

---

## 1. Introduction (0:00 - 0:30)
* **Visual:** Have your GitHub repo open showing the code.
* **Speaker:** "Hi, this is Trakr! When you run a Discord server with 5 or 6 different bots, it's impossible to know if one goes offline or stops working correctly. Trakr is a centralized observability pipeline that monitors ALL your bots in one place."
* **Speaker:** "We built a Python observer using the OpenTelemetry SDK. Every minute, it polls Discord for presence data, message activity, and audit logs, and pushes those metrics directly to SigNoz."

## 2. Dashboard Tour (0:30 - 1:30)
* **Visual:** Switch to SigNoz and open the **Bot Uptime & Reliability** dashboard.
* **Speaker:** "Here is our first dashboard. You can instantly see our SLA uptime and a timeline of any bot crashes."
* **Visual:** Switch to the **Bot Activity** and **Moderation Actions** dashboards.
* **Speaker:** "We also track exact throughput. If a bot starts spamming, or if our moderation bot starts kicking too many people, we see it immediately in these time-series and pie charts."
* **Visual:** Switch to the **Recovery Funnel** dashboard.
* **Speaker:** "This is our Recovery Funnel. It doesn't just show uptime; it cross-references crashes with message data to prove that a bot actually *resumed working* after it reconnected."

## 3. Alerts in Action (1:30 - 2:00)
* **Visual:** Switch to the **Triggered Alerts** tab in SigNoz (showing the Quiet Bot alerts firing).
* **Speaker:** "Finally, we set up three specific alerts: a threshold downtime alert, an absent-data pipeline alert, and this Anomaly alert for 'Quiet Bots'. Because my bots haven't sent a message in 10 minutes, their rate dropped below the baseline, and SigNoz automatically triggered these alerts for me."

## 4. Conclusion (2:00 - 2:15)
* **Visual:** Show the `alerts` folder in VS Code or GitHub.
* **Speaker:** "Trakr turns Discord bots from black boxes into fully observable microservices. Thanks for watching!"
