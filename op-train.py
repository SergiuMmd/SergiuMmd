import pip
import discord
import datetime
import asyncio
from random import randint
from discord.ext import commands
from discord import utils
import mysql.connector

capas = ["force", "endurance", "vitesse", "agilité", "précision", "combat", "arts", "armes", "fdd", "HDO", "HDA", "HDR"]
erreurCompré = """**Désolé mais je ne comprends pas ce que vous voulez améliorer.
Mettez une de ses statistiques comme dite ci-dessous:
force | endurance | vitesse | agilité | précision | arts | armes | combat | fdd | HDO | HDA | HDR**
"""
erreurCompré2 = """**Désolé mais je ne comprends pas ce que vous voulez baisser.
Mettez une de ses statistiques comme dite ci-dessous:
force | endurance | vitesse | agilité | précision | arts | armes | combat | fdd | HDO | HDA | HDR**
"""
admin_error_embed = discord.Embed(title="🔐 Permissions administrateur requise", description="Cette commande est réservée aux fondateurs / administrateurs / modérateurs", color=discord.Color.red())
ustat = ["endurance", "vitesse", "agilité", "précision", "combat", "arts", "armes", "fdd", "HDO", "HDA", "HDR"]

#SQL langage et Database 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ussent1001/rom34*",
  database="mydatabase"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE level (idd BIGINT UNIQUE, puissance TINYINT(150) DEFAULT 5, endurance TINYINT(150) DEFAULT 5, vitesse TINYINT(150) DEFAULT 5, agilité TINYINT(150) DEFAULT 5, précision TINYINT(150) DEFAULT 5, combat TINYINT(150) DEFAULT 5, arts TINYINT(150) DEFAULT 5, armes TINYINT(150) DEFAULT 5, fdd TINYINT(150) DEFAULT 0, HDO TINYINT(150) DEFAULT 0, HDA TINYINT(150) DEFAULT 0, HDR TINYINT(150) DEFAULT 0, blacklist BOOL DEFAULT 0, train DATE DEFAULT null)")
#mycursor.execute("CREATE TABLE pts (idd BIGINT UNIQUE, puissance TINYINT(100) DEFAULT 0, endurance TINYINT(100) DEFAULT 0, vitesse TINYINT(100) DEFAULT 0, agilité TINYINT(100) DEFAULT 0, précision TINYINT(100) DEFAULT 0, combat TINYINT(100) DEFAULT 0, arts TINYINT(100) DEFAULT 0, armes TINYINT(100) DEFAULT 0, fdd TINYINT(100) DEFAULT 0, HDO TINYINT(100) DEFAULT 0, HDA TINYINT(100) DEFAULT 0, HDR TINYINT(100) DEFAULT 0)")

#limites pouvoirs, à modifier en cas de besoin
def limite(capa, IDroles):
    if capa == "force":
        if 880492306027937862 in IDroles or 880791785599828028 in IDroles: #humain, skypiens
            return 100
        elif 880791784815468565 in IDroles or 880492684006010920 in IDroles or 880492684601593856 in IDroles or 880492685805355058 in IDroles or 914151004709191731 in IDroles: #surhomme, mink, fishman, cyborg, long-bras
            return 125
        elif 880492685146853416 in IDroles: #géant
            return 150
        else:
            return
    elif capa == "endurance":
        if 880492306027937862 in IDroles or 880791785599828028 in IDroles or 914151004709191731 in IDroles: #humain, skypien, long-bras 
            return 100
        elif 880791784815468565 in IDroles or 880492684006010920 in IDroles or 880492684601593856 in IDroles or 880492685805355058 in IDroles: #surhomme, mink, fishman, cyborg
            return 125
        elif 880492685146853416 in IDroles: #géant
            return 150
        else:
            return
    elif capa == "vitesse":
        if 880492685146853416 in IDroles or 880492684601593856 in IDroles or 880492685805355058 in IDroles: #géants, fishman, cyborgs
            return 100
        elif 880492306027937862 in IDroles or 880791784815468565 in IDroles or 880791785599828028 in IDroles or 914151004709191731 in IDroles: #humain, surhomme, skypien, long-bras
            return 125
        elif 880492684006010920 in IDroles: #mink
            return 150
        else:
            return
    elif capa == "agilité":
        if 880492685146853416 in IDroles or 880492684601593856 in IDroles or 880492685805355058 in IDroles or 914151004709191731 in IDroles: #géants, fishman, cyborg, long-bras
            return 100
        elif 880492306027937862 in IDroles or 880791784815468565 in IDroles or 880492684006010920 in IDroles: #homme, surhomme, mink
            return 125
        elif 880791785599828028 in IDroles: #skypien
            return 150
        else:
            return
    elif capa == "précision":
        if 880492684006010920 in IDroles or 880492685146853416 in IDroles or 880492684601593856 in IDroles or 914151004709191731 in IDroles: #mink, géant, fishman, long-bras
            return 100
        elif 880492306027937862 in IDroles or 880791784815468565 in IDroles or 880791785599828028 in IDroles: #homme, surhomme, skypien
            return 125
        elif 880492685805355058 in IDroles: #cyborg
            return 150
        else:
            return
    elif capa == "arts":
        if 880538619364909116 in IDroles:
            return 100
        elif 880538065414811668 in IDroles:
            return 125
        elif 880538064802414653 in IDroles:
            return 150
        else:
            return
    elif capa == "armes":
        if 880538064802414653 in IDroles:
            return 100
        elif 880538065414811668 in IDroles:
            return 125
        elif 880538619364909116 in IDroles:
            return 150
        else:
            return
    else:
        return 150

def check(m):
    if m.reference is not None:
         return True
    return False

def niveau(power):
    p1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    p2 = [55, 60, 65, 70, 75, 80, 85, 90, 95]
    p3 = [100, 105, 110, 115, 120, 125, 130]
    p4 = [135, 140, 145]
    if power in p1:
        return 2
    elif power in p2:
        return 3
    elif power in p3:
        return 4
    elif power in p4:
        return 5
    else:
        return None

def multiplicateur(capa):
    if capa == "force" or capa == "endurance" or capa == "vitese" or capa == "agilité" or capa == "précision":
        m = 1
    elif capa == "combat" or capa == "arts" or capa == "armes" or capa == "fdd":
        m = 2
    elif capa == "HDO" or capa == "HDA":
        m = 3
    else:
        m = 4
    return m

#à modifier les rôles admins
class Stats(commands.Cog):
    @commands.command()
    async def stats(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        if ctx.message.mentions == []:
            idd = ctx.message.author.id
        else:
            idd = ctx.message.mentions[0].id
        mycursor.execute("SELECT puissance, endurance, vitesse, agilité, précision, combat, arts, armes, fdd, HDO, HDA, HDR FROM level WHERE idd = " + str(idd))
        a = mycursor.fetchall()
        if len(a) == 0:
            d = "Désolé mais il semblerait que " + ctx.guild.get_member(idd).mention + " ne soit pas intégré dans la base de données du serveur."
            await ctx.send(embed=discord.Embed(title="❓Membre Introuvable dans la Base de Données", description=d, color=discord.Color.red()))
            return
        a = a[0]
        ti = "Statistiques de " + ctx.guild.get_member(idd).name + "#" + ctx.guild.get_member(idd).discriminator + ":"
        desc = "**Force :muscle: ➞ " + str(a[0]) + " %\n Endurance :leg: ➞ " + str(a[1]) + " %\n Vitesse :foot: ➞ " + str(a[2]) + " %\n Agilité :man_cartwheeling: ➞ " + str(a[3]) + " %\n Précision :eye: ➞ " + str(a[4]) + " %\n Maîtrise de Combat :punch: ➞ " + str(a[5]) + " %\n Maîtrise d'Arts Martiaux :martial_arts_uniform: ➞ " + str(a[6]) + " %\n Maîtrise d'Arme :dagger: ➞ " + str(a[7]) + " %\n Maîtrise du Pouvoir du FDD :melon: " + str(a[8]) + " %\n\n HDO :eyes: ➞ " + str(a[9]) + " %\n HDA :mechanical_arm: ➞ " + str(a[10]) + " %\n HDR :crown: ➞ " + str(a[11]) + "%**"
        await ctx.send(embed=discord.Embed(title=ti, description=desc, color=discord.Color.green()))
        return

    @commands.command()
    async def up(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        idd = ctx.author.id
        Lroles = ctx.guild.get_member(idd).roles
        IDroles = []
        admin = False
        for roles in Lroles:
            IDroles.append(roles.id)
        if 880495757604581417 in IDroles or 878962101903847445 in IDroles or 880486649191100477 in IDroles or idd == 539022078200774696:
            admin = True
        if admin == False:
            await ctx.send(embed=admin_error_embed)
            return
        contenu = str(ctx.message.content).split()
        if ctx.message.mentions != []:
            idd = ctx.message.mentions[0].id
        else:
            if contenu[1].isnumeric() == True:
                idd = int(contenu[1])
            else:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="La commande que vous avez inséré n'est pas bonne. Vérifiez si vous avez bien mentionné quelqu'un / inséré un ID valide.", color=discord.Color.red()))
                return
        if ctx.guild.get_member(idd) == None:
            await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="La personne que vous avez mentionné / l'ID que vous avez inséré n'est pas bon.\n->Vérifiez que vous avez bien mentionné la bonne personne / inséré le bon ID.\n->Vérifiez si la personne est présente sur ce serveur.", color=discord.Color.red()))
            return
        if len(contenu) != 3 and len(contenu) != 4:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semble que votre commande est erronée. Vérifiez bien que vous avez bien inséré le bon nombre de paramètres.", color=discord.Color.red()))
            return
        elif len(contenu) == 3:
            up = 5
        elif contenu[3].isnumeric() == True:
            up = int(contenu[3])*5
        else:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semblerait que le dernier paramètre de la commande ne soit pas un nombre entier. Veuillez en insérer un, ou ne rien insérer.", color=discord.Color.red()))
            return
        if contenu[2] == "force":
            mycursor.execute("SELECT puissance FROM level WHERE idd = " + str(idd))
            a = mycursor.fetchone()[0]
            up = up + a 
            mycursor.execute("UPDATE level SET puissance = " + str(up) + " WHERE idd = " + str(idd))
            mydb.commit()
            d = ctx.guild.get_member(idd).mention + " a reçu une amélioration en **force**!\n Il est passé d'une maîtrise de **" + str(a) + " %** à une maîtrise de **" + str(up) + " %**."
        elif contenu[2] in ustat:
            mycursor.execute("SELECT " + contenu[2] + " FROM level WHERE idd = " + str(idd))
            a = mycursor.fetchone()[0]
            up = up + a
            mycursor.execute("UPDATE level SET " + contenu[2] + " = " + str(up) + " WHERE idd = " + str(idd))
            d = ctx.guild.get_member(idd).mention + " a reçu une amélioration en **" + contenu[2] + "**!\n Il est passé d'une maîtrise de **" + str(a) + " %** à une maîtrise de **" + str(up) + " %**." 
        await ctx.send(embed=discord.Embed(title="⏫ Amélioration Effectuée", description=d, color=discord.Color.green()))
        return

    @commands.command()
    async def tlog(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        idd = ctx.author.id
        Lroles = ctx.guild.get_member(idd).roles
        IDroles = []
        admin = False
        for roles in Lroles:
            IDroles.append(roles.id)
        if 880495757604581417 in IDroles or 878962101903847445 in IDroles or 880486649191100477 in IDroles or idd == 539022078200774696:
            admin = True
        if admin == False:
            await ctx.send(embed=admin_error_embed)
            return
        idd = str(idd)
        #vérification sous-commande
        contenu = str(ctx.message.content).split()
        long = len(contenu)
        mat = False
        if ctx.message.mentions != [] and len(ctx.message.mentions) == 1:
            idd = ctx.message.mentions[0].id
            if ctx.guild.get_member(idd) == None:
                await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="La personne que vous avez mentionné / l'ID que vous avez inséré n'est pas bon.\n->Vérifiez que vous avez bien mentionné la bonne personne / inséré le bon ID.\n->Vérifiez si la personne est présente sur ce serveur.", color=discord.Color.red()))
                return
        elif len(contenu) == 2:
            mat = True
        elif len(ctx.message.mentions) > 1:
            await ctx.send(embed=discord.Embed(title="❌ Trop de Mentions", description="Veuillez ne mentionner qu'une seule personne s'il vous plaît / insérer un ID valide (sauf si la personne n'est plus sur le serveur.", color=discord.Color.red()))
            return
        elif contenu[2].isnumeric() == False:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="La commande que vous avez inséré n'est pas bonne. Vérifiez si vous avez bien mentionné quelqu'un / inséré un ID valide.", color=discord.Color.red()))
            return
        elif contenu[2].isnumeric() == True:
            idd = int(contenu[2])
            if ctx.guild.get_member(idd) == None:
                await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="La personne que vous avez mentionné / l'ID que vous avez inséré n'est pas bon.\n->Vérifiez que vous avez bien mentionné la bonne personne / inséré le bon ID.\n->Vérifiez si la personne est présente sur ce serveur.", color=discord.Color.red()))
                return
        if contenu[1] == "intégrer" and mat == False:
            mycursor.execute("INSERT INTO level (idd) VALUES (" + str(idd) + ")")
            mycursor.execute("INSERT INTO pts (idd) VALUES (" + str(idd) + ")")
            mydb.commit()
            d = ctx.guild.get_member(idd).mention + " a été intégré avec succès dans la base de donnée du bot!"
            await ctx.send(embed=discord.Embed(title="✅ Membre Intégré", description=d, color=discord.Color.green()))
            return
        elif contenu[1] == "retirer" and mat == False:
            mycursor.execute("DELETE FROM level WHERE idd = " + str(idd))
            mycursor.execute("DELETE FROM pts WHERE idd = " + str(idd))
            mydb.commit()
            d = "La personne a bien été retirée de la base de donnée du serveur (ID: **" + str(idd) + "**."
            await ctx.send(embed=discord.Embed(title="♻️ Membre Retiré", description=d, color=discord.Color.green()))
        elif contenu[1] == "nettoyer" and mat == True:
            mycursor.execute("SELECT idd FROM level")
            a = mycursor.fetchall()
            b = []
            for x in a:
                if ctx.guild.get_member(x[0]) == None:
                    b.append(x[0])  
            if len(b) == 0:
                await ctx.send(embed=discord.Embed(title="✅ Rien à Nettoyer", description="Il n'y a aucun membre à nettoyer!", color=discord.Color.orange()))
                return
            else:
                for c in b:
                    mycursor.execute("DELETE FROM level WHERE idd = " + str(c))
                    mycursor.execute("DELETE FROM pts WHERE idd = " + str(c))
                mydb.commit()
                d = "** " + str(len(b)) + "** personnes ont été retirées de la base de données car elles n'étaient pas présentes sur le serveur."
                await ctx.send(embed=discord.Embed(title="♻️ Nettoyage Effectué", description=d, color=discord.Color.green()))
                return
        elif contenu[1] == "baisser" and mat == False:
            if long == 4:
                deup = 5
            elif long == 5:
                if contenu[4].isnumeric() == False:
                    await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semblerait qu'il y ait un paramètre éroné inséré à la fin de la commande.", color=discord.Color.red()))
                    return
                deup = int(contenu[4])*5
            else:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semblerait qu'il y ait un paramètre en trop / en moins dans cette sous-commande.", color=discord.Color.red()))
                return
            if contenu[3] == "force":
                mycursor.execute("SELECT puissance FROM level WHERE idd = " + str(idd))
                a = mycursor.fetchone()[0]
                if a - deup <= 0:
                    deup = 0
                else:
                    deup = a - deup
                mycursor.execute("UPDATE level SET puissance = " + str(deup) + " WHERE idd = " + str(idd))
                mydb.commit()
                d = ctx.guild.get_member(idd).mention + " a bien été nerf en force!\n Il est tombé de **" + str(a) + " %** de maîtrise à **" + str(deup) + " %** de maîtrise."
                await ctx.send(embed=discord.Embed(title="📉 Nerf Effectué", description=d, color=discord.Color.green()))
                return
            elif contenu[3] in ustat:
                mycursor.execute("SELECT " + contenu[3] + " FROM level WHERE idd = " + str(idd))
                a = mycursor.fetchone()[0]
                if a - deup <= 0:
                    deup = 0
                else:
                    deup = a - deup
                mycursor.execute("UPDATE level SET " + contenu[3] + " = " + str(deup) + " WHERE idd = " + str(idd))
                mydb.commit()
                d = ctx.guild.get_member(idd).mention + " a bien été nerf en " + contenu[3] + "!\n Il est tombé de **" + str(a) + " %** de maîtrise à **" + str(deup) + " %** de maîtrise."
                await ctx.send(embed=discord.Embed(title="📉 Nerf Effectué", description=d, color=discord.Color.green()))
                return
            else:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semblerait qu'il y ait une erreur au niveau de la capacité à nerf.", color=discord.Color.red()))
                return
        else:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semblerait qu'il y ait une erreur au niveau du premier paramètre définissant la commande à exécuter.", color=discord.Color.red()))
            return

    @commands.command()
    async def entraînement(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        idd = ctx.author.id
        rôles = ctx.guild.get_member(idd).roles
        lrôles = []
        for role in rôles:
            lrôles.append(role.id)
        if 880495137699004476 not in lrôles:
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite aux Sans-Fiches", description="Désolé mais il semblerait que vous n'ayez pas fait votre fiche sur le serveur. Par conséquent, vous ne pouvez pas effectuer des entraînements sur ce serveur.", color=discord.Color.red()))
            return
        mycursor.execute("SELECT blacklist FROM level WHERE idd = " + str(idd))
        a = mycursor.fetchone()[0]
        if a == 0:
            a = False
        else:
            a = True
        if a == True:
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite aux Blacklistés", description="Désolé mais il semblerait que vous soyez blacklisté sur ce serveur. Par conséquent, vous ne pouvez pas effectuer d'entraînements!", color=discord.Color.red()))
            return
        J = datetime.datetime.now()
        jour = str(J.year) + "-" + str(J.month) + "-" + str(J.day)
        mycursor.execute("SELECT train FROM level WHERE idd = " + str(idd))
        b = str(mycursor.fetchone()[0])
        if jour == b:
            await ctx.send(embed=discord.Embed(title="⛔ Entraînement Journalier Déjà Effectué", description="Désolé mais vous avez déjà effectué un entraînement aujourd'hui.", color=discord.Color.red()))
            return
        else:
            pass
        contenu = str(ctx.message.content).split()
        long = len(contenu)
        if long == 2:
            message = ctx.message
            if check(message) == True:
                message = message.reference.resolved
                if message.author != ctx.author:
                    await ctx.send(embed=discord.Embed(title="🚔 Vol d'Entraînement", description="Le vol d'entraînement n'est pas autorisé sur ce serveur. Veuillez ne plus recommencer s'il vous plaît, sinon vous serez blacklisté.", color=discord.Color.red()))
                    return
                message = message.content
                if len(message) < 150:
                    await ctx.send(embed=discord.Embed(title="❌ Entraînement Trop Court", description="Désolé mais votre entraînement est trop court! Veuillez l'agrandir s'il vous plaît.", color=discord.Color.red()))
                    return
                bonus = 0
                if 914169474633060352 in lrôles:
                    bonus += 2
                if 912595102961139743 in lrôles:
                    bonus += 1
                tpts = (randint(1,4) + bonus)*2
                if contenu[1] == "force":
                    mycursor.execute("SELECT puissance FROM level WHERE idd = " + str(idd))
                    powpin = mycursor.fetchone()[0]
                    mycursor.execute("SELECT puissance FROM pts WHERE idd = " + str(idd))
                    ptpin = mycursor.fetchone()[0]
                    lim = limite("force", lrôles)
                elif contenu[1] in ustat:
                    mycursor.execute("SELECT " + contenu[1] + " FROM level WHERE idd = " + str(idd))
                    powpin = mycursor.fetchone()[0]
                    mycursor.execute("SELECT " + contenu[1] + " FROM pts WHERE idd = " + str(idd))
                    ptpin = mycursor.fetchone()[0]
                    lim = limite(contenu[1], lrôles)
                else:
                    await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Veuillez insérer une capacité valide à entraîner. Sélectionnez une parmis:\n force | endurance | vitesse | agilité | précision | combat | arts | armes | fdd | HDO | HDA | HDR .", color=discord.Color.red()))
                    return
                if niveau(powpin) == None:
                    await ctx.send(embed=discord.Embed(title="❌ Capacité Interdite", description="Désolé mais il semblerait que vous n'ayez pas le droit d'entraîner cette capacité. Cela est normal quand il s'agit des hakis alors que vous ne connaissez même pas leur existence / ne les avaient pas déjà entraînés avec un maître / lorsque vous ne les avaient pas éveillé.", color=discord.Color.red()))
                    return
                end = False
                ptot = tpts + ptpin
                powf = powpin
                while end == False:
                    ptot -= niveau(powf)*multiplicateur(contenu[1])
                    if ptot < 0:
                        ptot += niveau(powf)*multiplicateur(contenu[1])
                        end = True
                    else:
                        if powf < lim:
                            powf += 5
                        else:
                            end = True
                pn = niveau(powf)*multiplicateur(contenu[1])
                if contenu[1] == "force":
                    mycursor.execute("UPDATE level SET puissance = " + str(powf) + " WHERE idd = " + str(idd))
                    mycursor.execute("UPDATE pts SET puissance = " + str(ptot) + " WHERE idd = " + str(idd))
                else:
                    mycursor.execute("UPDATE level SET " + contenu[1] + " = " + str(powf) + " WHERE idd = " + str(idd))
                    mycursor.execute("UPDATE pts SET " + contenu[1] + " = " + str(ptot) + " WHERE idd = " + str(idd))
                mycursor.execute("UPDATE level SET train = '" + jour + "' WHERE idd = " + str(idd))
                mydb.commit()
                if powpin == powf:
                    d = "Votre entraînement en " + contenu[1] + " a été effectué avec succès!\n Vous avez obtenu **" + str(tpts) + " points** dans cette capacité mais votre capacité reste toujours à **" + str(powf) + " %** de maîtrise."
                    bup = ""
                else:
                    d = "Votre entraînement en " + contenu[1] + " a été effectué avec succès!\n Vous avez obtenu **"  + str(tpts) + " points** dans cette capacité!\n Vous êtes passé de **" + str(powpin) + " %** de maîtrise à **" + str(powf) + " %** de maîtrise dans cette capacité!"
                    bup = "\nSa maîtrise est passée de **" + str(powpin) + " %** à **" + str(powf) + " %**."
                await ctx.send(embed=discord.Embed(title="💪 Entraînement Effectué", description=d, color=discord.Color.green()))
                ti = "Entraînement de " + ctx.guild.get_member(idd).name + "#" + str(ctx.guild.get_member(idd).discriminator) + " en " + contenu[1] + " :"
                desc = "Cette personne a obtenu **" + str(tpts) + " points** dans cette capacité. Elle a maintenant **" + str(ptot) + " / " + str(pn) + " points** dans cette capacité." + bup + "\n Voici son entraînement:\n``` ```" + message + "\n ``` ```"
                await ctx.guild.get_channel(882254013968568390).send(embed=discord.Embed(title=ti, description=desc, color=discord.Color.blue()))
                return
            else:
                await ctx.send(embed=discord.Embed(title="❌ Entraînement Non-Replié", description="Désolé mais il semblerait que vous n'ayez pas répondu à votre entraînement. Veuillez le faire avec cette commande pour pouvoir faire votre entraînement s'il vous plaît.", color=discord.Color.red()))
                return
        else:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais il semblerait que vous n'ayez pas inséré une capacité à entraîner. Veuillez en insérer une parmis celles-ci:\n force | endurance | vitesse | agilité | précision | combat | arts | armes | fdd | HDO | HDA | HDR .", color=discord.Color.red()))
            return

    @commands.command()
    async def blacklist(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        idd = ctx.author.id
        Lroles = ctx.guild.get_member(idd).roles
        IDroles = []
        admin = False
        for roles in Lroles:
            IDroles.append(roles.id)
        if 880495757604581417 in IDroles or 878962101903847445 in IDroles or 880486649191100477 in IDroles or idd == 539022078200774696:
            admin = True
        if admin == False:
            await ctx.send(embed=admin_error_embed)
            return
        message = str(ctx.message.content).split()
        if len(message) != 3:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais il semblerait qu'il y ait un paramètre manquant.\n Vérifiez bien que vous avez mentionné quelqu'un / inséré un ID ET que vous avez ajouté une durée valide de blacklist (en secondes (s), minutes (m), heures (h), jours(j), semaines(w)).", color=discord.Color.red()))
            return
        if ctx.message.mentions == []:
            if message[1].isnumeric() == False:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais je ne comprends pas votre commande. Veuillez mentionner quelqu'un dans la premier paramètre / insérer un ID valide.", color=discord.Color.red()))
                return
            else:
                if ctx.guild.get_member(int(message[1])) == None:
                    await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="Désolé mais l'ID que vous avez insérer est invalide car la personne en question a quitté le serveur.", color=discord.Color.red()))
                    return
                else:
                    idd = int(message[1])
        else:
            idd = ctx.message.mentions[0].id
            if ctx.guild.get_member(idd) == None:
                await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="Désolé mais il semblerait que la personne que vous venez de mentionner n'est pas présente sur le serveur.", color=discord.Color.red()))
                return
        mycursor.execute("SELECT blacklist FROM level WHERE idd = " + str(idd))
        a = mycursor.fetchone()[0]
        if a == 1:
            d = ctx.guild.get_member(idd).mention + " est déjà blacklisté."
            await ctx.send(embed=discord.Embed(title="🔒 Membre Déjà Blacklisté ✅", description=d, color=discord.Color.green()))
            return
        #vérification durée
        msg = message[2]
        if msg[-1] == "w":
            msg = msg[:-1]
            multi = 604800 #nombre de secondes en 1 semaine
        elif msg[-1] == "j":
            msg = msg[:-1]
            multi = 86400 #nombre de secondes en 1 jour
        elif msg[-1] == "h":
            msg = msg[:-1]
            multi = 3600
        elif msg[-1] == "m":
            msg = msg[:-1]
            multi = 60
        elif msg[-1] == "s":
            msg = msg[:-1]
            multi = 1
        elif message[-1].isnumeric() == True:
            multi = 1
        else:
            await ctx.send(embed=discord.Embed(title="❌ Durée Invalide", description="Désolé mais la durée que vous avez inséré est invalide. Veuillez en insérer une avec un nombre entier devant et avec une lettre à la fin désignant la durée (s en secondes, m en minutes, h en heures, j en jours et w en semaines).", color=discord.Color.red()))
            return
        attend = int(msg) * multi
        mycursor.execute("UPDATE level SET blacklist = 1 WHERE idd = " + str(idd))
        mydb.commit()
        await ctx.send(embed=discord.Embed(title="🔒 Membre Blacklisté", description="La personne en question a bien été blacklistée!"))
        await asyncio.sleep(attend)
        if ctx.guild.get_member(idd) == None:
            mycursor.execute("DELETE FROM level WHERE idd = " + str(idd))
            mycursor.execute("DELETE FROM pts WHERE idd = " + str(idd))
            mydb.commit()
            return
        mycursor.execute("UPDATE level SET blacklist = 0 WHERE idd = " + str(idd))
        mydb.commit()
        d = ctx.guild.get_member(idd).mention + " ( **" + ctx.guild.get_member(idd).name + "#" + ctx.guild.get_member(idd).discriminator + "** ) a été retiré avec succès de la liste noire du serveur!"
        await ctx.guild.get_channel(880487562219782154).send(embed=discord.Embed(title="🔒 Membre Déblacklisté", description=d, color=discord.Color.green()))
        return
    
    @commands.command()
    async def deblacklist(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        idd = ctx.author.id
        Lroles = ctx.guild.get_member(idd).roles
        IDroles = []
        admin = False
        for roles in Lroles:
            IDroles.append(roles.id)
        if 880495757604581417 in IDroles or 878962101903847445 in IDroles or 880486649191100477 in IDroles or idd == 539022078200774696:
            admin = True
        if admin == False:
            await ctx.send(embed=admin_error_embed)
            return
        message = str(ctx.message.content).split()
        if len(message) != 2:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais il semblerait qu'il y ait un paramètre manquant.\n Vérifiez bien que vous avez mentionné quelqu'un / inséré un ID ET que vous avez ajouté une durée valide de blacklist (en secondes (s), minutes (m), heures (h), jours(j), semaines(w)).", color=discord.Color.red()))
            return
        if ctx.message.mentions == []:
            if message[1].isnumeric() == False:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais je ne comprends pas votre commande. Veuillez mentionner quelqu'un dans la premier paramètre / insérer un ID valide.", color=discord.Color.red()))
                return
            else:
                if ctx.guild.get_member(int(message[1])) == None:
                    await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="Désolé mais l'ID que vous avez insérer est invalide car la personne en question a quitté le serveur.", color=discord.Color.red()))
                    return
                else:
                    idd = int(message[1])
        else:
            idd = ctx.message.mentions[0].id
            if ctx.guild.get_member(idd) == None:
                await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="Désolé mais il semblerait que la personne que vous venez de mentionner n'est pas présente sur le serveur.", color=discord.Color.red()))
                return
        mycursor.execute("SELECT blacklist FROM level WHERE idd = " + str(idd))
        a = mycursor.fetchone()[0]
        if a == 0:
            d = ctx.guild.get_member(idd).mention + " n'est pas dans la liste noire."
            await ctx.send(embed=discord.Embed(title="✅ Membre Non Blacklisté ", description=d, color=discord.Color.green()))
            return
        else:
            mycursor.execute("UPDATE level SET blacklist = 0 WHERE idd = " + str(idd))
            mydb.commit()
            d = ctx.guild.get_member(idd).mention + " a été retiré de la liste noire avec succès."
            await ctx.send(embed=discord.Embed(title="✅ Membre Déblacklisté ", description=d, color=discord.Color.green()))
            return

    @commands.command()
    async def tpts(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        idd = ctx.author.id
        Lroles = ctx.guild.get_member(idd).roles
        IDroles = []
        admin = False
        for roles in Lroles:
            IDroles.append(roles.id)
        if 880495757604581417 in IDroles or 878962101903847445 in IDroles or 880486649191100477 in IDroles or idd == 539022078200774696:
            admin = True
        if admin == False:
            await ctx.send(embed=admin_error_embed)
            return
        message = str(ctx.message.content).split()
        if len(message) != 4 and len(message) != 5:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il semble que votre commande est erronée. Vérifiez bien que vous avez bien inséré le bon nombre de paramètres.", color=discord.Color.red()))
            return
        if ctx.message.mentions == []:
            if message[2].isnumeric() == False:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais je ne comprends pas votre commande. Veuillez mentionner quelqu'un dans la premier paramètre / insérer un ID valide.", color=discord.Color.red()))
                return
            else:
                if ctx.guild.get_member(int(message[2])) == None:
                    await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="Désolé mais l'ID que vous avez insérer est invalide car la personne en question a quitté le serveur.", color=discord.Color.red()))
                    return
                else:
                    idd = int(message[2])
        else:
            idd = ctx.message.mentions[0].id
            if ctx.guild.get_member(idd) == None:
                await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description="Désolé mais il semblerait que la personne que vous venez de mentionner n'est pas présente sur le serveur.", color=discord.Color.red()))
                return
        if message[1] == "ajouter":
            operator = 1
            sup = "reçu"
        elif message[1] == "retirer":
            operator = -1
            sup = "perdu"
        else:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Sous-Commande", description="Désolé mais il semblerait qu'il y ait une erreur au niveau du premier paramètre définissant la sous-commande à exécuter.\n Veuillez insérer soit **ajouter**, soit **retirer** dans le premier paramètre.", color=discord.Color.red()))
            return
        if message[3] == "force":
            mycursor.execute("SELECT puissance FROM pts WHERE idd = " + str(idd))
            ptd = mycursor.fetchone()[0]
            mycursor.execute("SELECT puissance FROM level WHERE idd = " + str(idd))
            lvl = mycursor.fetchone()[0]
            sta = "puissance"
        elif message[3] in ustat:
            mycursor.execute("SELECT " + message[3] + " FROM pts WHERE idd = " + str(idd))
            ptd = mycursor.fetchone()[0]
            mycursor.execute("SELECT " + message[3] + " FROM pts WHERE idd = " + str(idd))
            lvl = mycursor.fetchone()[0]
            sta = message[3]
        else:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Capacité", description="Désolé mais la capacité que vous avez inséré est invalide. Veuillez insérer une capacité valide parmis:\n force | endurance | vitesse | agilité | précision | combat | arts | armes | fdd | HDO | HDA | HDR.", color=discord.Color.red()))
            return
        if len(message) == 4:
            pta = 1
        elif message[4].isnumeric() == False:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais le nombre de points final à ajouter que vous avez inséré dans le dernier paramètre est invalide. Veuillez insérer un nombre entier à la fin de la commande s'il vous plaît.", color=discord.Color.red()))
            return
        else:
            pta = int(message[4])
        end = False
        powf = lvl
        ptot = ptd + pta*operator
        if ptot < 0:
            ptot = 0
            end = True
        lim = limite(message[3], IDroles)
        while end == False:
            ptot -= niveau(powf)*multiplicateur(message[3])
            if ptot < 0:
                ptot += niveau(powf)*multiplicateur(message[3])
                end = True
            else:
                if powf < lim:
                    powf += 5
                else:
                    end = True
        pn = niveau(powf)*multiplicateur(message[3])
        mycursor.execute("UPDATE level SET " + sta + " = " + str(powf) + " WHERE idd = " + str(idd))
        mycursor.execute("UPDATE pts SET " + sta + " = " + str(ptot) + " WHERE idd = " + str(idd))
        mydb.commit()
        if lvl == powf:
            ti = "✅ Ajout Effectué"
            d = ctx.guild.get_member(idd).mention + " a bien " + sup + " **" + str(pta) + " points** en **" + message[3] + "**.\n Il a maintenant **" + str(ptot) + " / " + str(pn) + " points** dans cette capacité."
        else:
            ti = "✅ Ajout Effectué ⏫"
            d = ctx.guild.get_member(idd).mention + " a bien " + sup + " **" + str(pta) + " points** en **" + message[3] + "**.\n Il a maintenant **" + str(ptot) + " / " + str(pn) + " points** dans cette capacité.\n En plus de cela, il est passé de **" + str(lvl) + " %** de maîtrise à **" + str(powf) + " %** de maîtrise dans cette capacité."
        await ctx.send(embed=discord.Embed(title=ti, description=d, color=discord.Color.green()))
        return

def setup(client):
    client.add_cog(Stats(client))