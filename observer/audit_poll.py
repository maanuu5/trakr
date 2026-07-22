import discord
from discord.ext import tasks
import store

def setup_audit_poll(client, meter, logger):
    mod_actions_counter = meter.create_counter("trakr.bot.mod_actions")

    @tasks.loop(minutes=2)
    async def poll_audit_logs():
        for guild in client.guilds:
            try:
                last_id = store.get_last_audit_id(str(guild.id))
                
                # If first run, just grab the latest 1 entry to seed the watermark
                if last_id is None:
                    async for entry in guild.audit_logs(limit=1):
                        store.set_last_audit_id(str(guild.id), entry.id)
                    continue

                new_entries = []
                # Fetch entries chronologically after our last seen ID
                async for entry in guild.audit_logs(limit=100, after=discord.Object(id=last_id)):
                    new_entries.append(entry)
                
                if not new_entries:
                    continue
                    
                # Ensure we process chronologically (oldest to newest)
                new_entries.sort(key=lambda e: e.id)
                
                for entry in new_entries:
                    # We only care about actions taken by bots
                    if entry.user and entry.user.bot:
                        action_type = str(entry.action).replace("AuditLogAction.", "")
                        
                        # Make the action names more human-readable
                        if action_type == "member_update":
                            if hasattr(entry.after, "timed_out_until") or hasattr(entry.after, "communication_disabled_until"):
                                action_type = "timeout"
                                
                        attrs = {
                            "bot.name": entry.user.name,
                            "bot.id": str(entry.user.id),
                            "action_type": action_type
                        }
                        mod_actions_counter.add(1, attrs)
                        
                        target = getattr(entry.target, "name", str(entry.target))
                        log_msg = f"{entry.user.name} performed {action_type} on {target}"
                        logger.info(log_msg, extra=attrs)
                        print(f"[audit] {log_msg}")

                # Update watermark to the newest processed ID
                store.set_last_audit_id(str(guild.id), new_entries[-1].id)

            except discord.Forbidden:
                print(f"[audit] Missing View Audit Log permission in {guild.name}")
            except Exception as e:
                logger.exception(f"Error polling audit logs for {guild.name}")

    @poll_audit_logs.before_loop
    async def before_poll():
        await client.wait_until_ready()

    return poll_audit_logs
