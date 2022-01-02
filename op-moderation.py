import discord
import json
from discord import utils
import os
import random
import requests
import datetime
import asyncio
import io
from discord.ext import commands
import time


def avatar(user):
    return f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=4096"


def dict_permissions(permissions):
    return dict(zip([perm for perm, value in permissions], [value for perm, value in permissions]))


utils.dict_permissions = dict_permissions


admin_error_embed = discord.Embed(title="Permissions administrateur requise",
                                  description="Cette commande est réservée aux administrateurs", color=discord.Color.red())


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.locked_chans = []
        self.periods = {
            'minute': 60,
            'hour': 60**2,
            'day': 60**2*24
        }
        self.TENOR_API_KEY = "0KV5UBQZ40GC"

    @commands.Cog.listener()
    async def on_ready(self):
        self.mute_role = self.client.guild.get_role(798588493751517215)

    @commands.command(name="logs", aliases=['log', 'logging'])
    async def logs(self, ctx, channel: discord.TextChannel = None):
        if not ctx.channel.permissions_for(ctx.message.author).administrator:
            await ctx.send(embed=admin_error_embed)
            return

        if not self.client.log_channel and not channel:
            await ctx.send(embed=discord.Embed(title="Channel de logging non défini", description="Définissez un salon de logging via la comande ``log #salon``", color=discord.Color.red()))
            return

        if not channel:
            await ctx.send(embed=discord.Embed(title="Channel de logging", description=f"L'actuel salon de logging est {self.client.log_channel.mention}", color=discord.Color.green(), url=f'https://discord.com/channels/{ctx.guild.id}/{self.client.log_channel.id}'))
            return

        self.client.log_channel = channel
        await ctx.send(embed=discord.Embed(title="Nouveau channel de logging", description=f"Le nouveau salon de logging est {self.client.log_channel.mention}", color=discord.Color.green(), url=f'https://discord.com/channels/{ctx.guild.id}/{self.client.log_channel.id}'))
        await self.client.log_channel.send(embed=discord.Embed(title="Nouveau channel de logging", description=f"Ce salon sera désormais le salon de log.", color=discord.Color.green()))

    @commands.command(name="unmute", aliases=['unjail', 'reviens'])
    async def unmute(self, ctx, user: discord.User = None, *reason):
        reson = " ".join(reason)
        if not ctx.channel.permissions_for(ctx.message.author).administrator:
            await ctx.send(embed=admin_error_embed)
            return
        if not user:
            await ctx.send(embed=discord.Embed(title="Veuillez préciser un membre", description="La commande ``mute`` nécessite au minimum un membre à mute.", color=discord.Color.red()))
            return

        if not self.mute_role in ctx.guild.get_member(user.id).roles:
            await ctx.send(embed=discord.Embed(title="Membre non mute", description="La commande ``unmute`` ne s'effectue pas sur un membre non mute.", color=discord.Color.red()))

        await ctx.channel.guild.get_member(user.id).remove_roles(self.mute_role)

        if self.client.log_channel:
            embed = discord.Embed(
                title="Unmute", description=f"{user.mention} unmute dans {ctx.channel.mention} par {ctx.message.author.name}.", color=discord.Color.orange())

            if reason:
                embed.add_field(name='Raison', value=" ".join(reason))
            else:
                embed.add_field(name='Raison', value=f'``Non précisée``')

            await self.client.log_channel.send(embed=embed)

        embed = discord.Embed(
            title="Unmute", description=f"{user.mention} a bien été unmute.", color=discord.Color.green())
        if reason:
            embed.add_field(name='Raison', value=" ".join(reason))
        else:
            embed.add_field(name='Raison', value=f'``Non précisée``')
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="mute", aliases=['jail', 'tg'])
    async def mute(self, ctx, user: discord.User = None, *args):
        if len(args) >= 3:
            reason = args[:-2]
            period = args[-1]
            amount = args[-2]
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send(embed=discord.Embed(title="Veuillez préciser un nombre et une période valide", description="La commande ``mute`` nécessite un nombre et une période, sinon aucun des deux. \nExemple : ``mute @user 2 hour``\nLes périodes sont : ``minute``, ``hour``, et ``day``", color=discord.Color.red()))
                return
        elif len(args) in range(1, 3):
            reason = args
            period, amount = None, None
        else:
            period, amount, reason = None, None, ""

        if not ctx.channel.permissions_for(ctx.message.author).administrator:
            await ctx.send(embed=admin_error_embed)
            return
        if not user:
            await ctx.send(embed=discord.Embed(title="Veuillez préciser un membre", description="La commande ``mute`` nécessite au minimum un membre à mute.", color=discord.Color.red()))
            return

        if self.mute_role in ctx.guild.get_member(user.id).roles:
            await ctx.send(embed=discord.Embed(title="Membre déja mute", description="La commande ``mute`` ne s'effectue pas sur un membre déja mute.", color=discord.Color.red()))
            return

        if (not bool(amount) == bool(period)):
            await ctx.send(embed=discord.Embed(title="Veuillez préciser un nombre et une période valide", description="La commande ``mute`` nécessite un nombre et une période, sinon aucun des deux. \nExemple : ``mute @user 2 hour``\nLes périodes sont : ``minute``, ``hour``, et ``day``", color=discord.Color.red()))
            return

        await ctx.channel.guild.get_member(user.id).add_roles(self.mute_role)

        delay = 0
        if amount and period:
            if not period in self.periods:
                await ctx.send(embed=discord.Embed(title="Veuillez préciser un nombre et une période valide", description="La commande ``mute`` nécessite un nombre et une période, sinon aucun des deux. \nExemple : ``mute @user 2 hour``\nLes périodes sont : ``minute``, ``hour``, et ``day``", color=discord.Color.red()))
                return
            delay = amount*self.periods[period]
        if self.client.log_channel:
            embed = discord.Embed(
                title="Mute", description=f"{user.mention} mute dans {ctx.channel.mention} par {ctx.message.author.name}.", color=discord.Color.orange())
            if delay:
                embed.add_field(name='Durée', value=f'{amount} {period}')
            else:
                embed.add_field(name='Durée', value=f'``Indéterminée``')
            if reason:
                embed.add_field(name='Raison', value=" ".join(reason))
            else:
                embed.add_field(name='Raison', value=f'``Non précisée``')

            await self.client.log_channel.send(embed=embed)

        embed = discord.Embed(
            title="Mute", description=f"{user.mention} a bien été mute.", color=discord.Color.green())
        if delay:
            embed.add_field(name='Durée', value=f'{amount} {period}')
        else:
            embed.add_field(name='Durée', value=f'``Indéterminée``')
        if reason:
            embed.add_field(name='Raison', value=" ".join(reason))
        else:
            embed.add_field(name='Raison', value=f'``Non précisée``')
        await ctx.send(embed=embed, delete_after=5)
        if delay:
            await asyncio.sleep(delay)
            await ctx.channel.guild.get_member(user.id).remove_role(self.mute_role)
            await ctx.send(embed=discord.Embed(title="Unmute", description=f"{user.mention} n'est plus mute.", color=discord.Color.green()))
            if self.client.log_channel:
                embed = discord.Embed(
                    title="Unmute", description=f"{user.mention} unmute après {delay} heures de mute causées par {ctx.message.author.name}", color=discord.Color.green())
                await self.client.log_channel.send(embed=embed)

    @commands.command(name="kick", aliases=['expluse'])
    async def kick(self, ctx, user: discord.User = None, *args):
        reason = " ".join(args)
        if not ctx.channel.permissions_for(ctx.message.author).administrator:
            await ctx.send(embed=admin_error_embed)
            return
        
        if not user:
            await ctx.send(embed=discord.Embed(title="Veuillez préciser un membre", description="La commande ``kick`` nécessite au minimum un membre à expulser.", color=discord.Color.red()))
            return

        await ctx.channel.guild.get_member(user.id).kick()

        if self.client.log_channel:
            embed = discord.Embed(
                title="Kick", description=f"{user.mention} expulsé dans {ctx.channel.mention} par {ctx.message.author.name}.", color=discord.Color.orange())
            if reason:
                embed.add_field(name='Raison', value=" ".join(reason))
            else:
                embed.add_field(name='Raison', value=f'``Non précisée``')

            await self.client.log_channel.send(embed=embed)

        embed = discord.Embed(
            title="Kick", description=f"{user.mention} a bien été expulsé.", color=discord.Color.green())
        if reason:
            embed.add_field(name='Raison', value=" ".join(reason))
        else:
            embed.add_field(name='Raison', value=f'``Non précisée``')
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="ban", aliases=['bann'])
    async def ban(self, ctx, user: discord.User = None, *args):
        reason = " ".join(args)
        if not ctx.channel.permissions_for(ctx.message.author).administrator:
            await ctx.send(embed=admin_error_embed)
            return
        
        if not user:
            await ctx.send(embed=discord.Embed(title="Veuillez préciser un membre", description="La commande ``ban`` nécessite au minimum un membre à bannir.", color=discord.Color.red()))
            return

        await ctx.channel.guild.get_member(user.id).ban()

        if self.client.log_channel:
            embed = discord.Embed(
                title="Ban", description=f"{user.mention} banni dans {ctx.channel.mention} par {ctx.message.author.name}.", color=discord.Color.orange())
            if reason:
                embed.add_field(name='Raison', value=" ".join(reason))
            else:
                embed.add_field(name='Raison', value=f'``Non précisée``')

            await self.client.log_channel.send(embed=embed)

        embed = discord.Embed(
            title="Ban", description=f"{user.mention} a bien été banni.", color=discord.Color.green())
        if reason:
            embed.add_field(name='Raison', value=" ".join(reason))
        else:
            embed.add_field(name='Raison', value=f'``Non précisée``')
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="clear", aliases=['purge', 'nuke'])
    async def clear(self, ctx, amount: int = None):
        if not ctx.channel.permissions_for(ctx.message.author).administrator:
            await ctx.send(embed=admin_error_embed)
            return
        if not amount:
            await ctx.send(embed=discord.Embed(title="Veuillez préciser un montant", description="La commande clear nécessite un nombre de messages à supprimer.", color=discord.Color.red()))
            return
        nuke = (ctx.invoked_with == "nuke")
        
        if nuke:
            
            gif = random.randint(0, 10)
            if gif == 10:
                gif = "https://images-ext-1.discordapp.net/external/p4_oiLLAGmYNs3RNNcxRcDbrVzr2KAboDTea510kaVo/https/c.tenor.com/kUPteWkr3SEAAAAM/creeper-blast.gif"
            else:
                r = requests.get(f"https://g.tenor.com/v1/search?q=nuclear+explosion&key={self.TENOR_API_KEY}&limit=10")
                response = json.loads(r.content)
                gif=response['results'][gif]['media'][0]['gif']['url']
            
            count_msg = await ctx.send("Nuke coming...")
            for i in range(10, 0, -1):
                await count_msg.edit(content=f"**{i}**")
                await asyncio.sleep(1)
            
        purged = await ctx.channel.purge(limit=amount+2)
        if not nuke:
            embed = discord.Embed().set_author(
            name=f"{len(purged)} messages supprimés", icon_url=avatar(ctx.message.author))
            embed.colour = discord.Color.green()
            msg = await ctx.send(embed=embed)
        else:
            msg = await ctx.send(gif)
        
        if self.client.log_channel:
            embed = discord.Embed(
                title="Message Purge", description=f"{ctx.message.author.name} a purge {len(purged)} messages dans {ctx.channel.mention}.", color=discord.Color.orange())
            await self.client.log_channel.send(embed=embed)
            
        if not nuke:
            await asyncio.sleep(3.0)
            await msg.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            if message.embeds:
                if message.embeds[0].to_dict()['type'] == 'image':
                    return
                embed = message.embeds[0].set_footer(
                        text=datetime.datetime.now().strftime('%d/%m/%y | %H:%M:%S'))
                await message.edit(embed=embed, supress=True)
                
            return
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # check locked chans
        involved_channels = [
            chan for chan in self.locked_chans if chan.guild == member.guild]
        for channel in involved_channels:
            channel.set_permissions(member, send_messages=False)


def setup(client):
    client.add_cog(Moderation(client))
