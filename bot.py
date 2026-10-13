import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🟢 {bot.user} est désormais EN LIGNE !')
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commande(s) synchronisée(s).")
    except Exception as e:
        print(f"Erreur de synchro : {e}")

@bot.tree.command(name="creer_groupe", description="Crée un groupe illégal avec un salon textuel et vocal privé.")
@app_commands.describe(nom="Nom du groupe", membre1="Premier membre")
async def creer_groupe(
    interaction: discord.Interaction, 
    nom: str, 
    membre1: discord.Member, 
    membre2: discord.Member = None, 
    membre3: discord.Member = None
):
    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild

    try:
        # Cherche si une catégorie "🔒│GROUPES ILLÉGAUX" existe déjà sur le serveur
        category = discord.utils.get(guild.categories, name="🔒│GROUPES ILLÉGAUX")
        
        # Si elle n'existe pas, le bot la crée automatiquement proprement
        if not category:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False)
            }
            category = await guild.create_category("🔒│GROUPES ILLÉGAUX", overwrites=overwrites)

        # Création du rôle du groupe
        role = await guild.create_role(name=f"Groupe - {nom}", color=discord.Color.dark_grey())

        # Rassemblement des membres
        membres_groupe = [interaction.user, membre1]
        for m in [membre2, membre3]:
            if m:
                membres_groupe.append(m)

        for m in membres_groupe:
            await m.add_roles(role)

        # Permissions des salons privés pour le groupe
        overwrites_salons = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            role: discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True, speak=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
        }

        # Création des salons dans la catégorie
        text_channel = await guild.create_text_channel(f"💬│{nom}", category=category, overwrites=overwrites_salons)
        voice_channel = await guild.create_voice_channel(f"🔊│{nom}", category=category, overwrites=overwrites_salons)

        await interaction.followup.send(
            f"✅ Le groupe **{nom}** a été créé avec succès !\n"
            f"• Salon textuel : {text_channel.mention}\n"
            f"• Salon vocal : {voice_channel.mention}",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Une erreur s'est produite : {e}", ephemeral=True)

import os

# ... (tout le reste de ton code reste identique au dessus) ...

# Récupère le token de manière sécurisée depuis l'hébergeur
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)