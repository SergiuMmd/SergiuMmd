import random
import pip
import datetime
import asyncio
import discord
from discord.ext import commands
from discord import utils
import mysql.connector

#entrepôt
moneydoc = {} #dict qui regroupe les RPlayers et leur argent.
incomedoc = {} #dict qui regroupe les RPlayers et leur revenus.
endettés = []
#embed
admin_error_embed = discord.Embed(title="🔐 Permissions administrateur requise", description="Cette commande est réservée aux fondateurs / administrateurs / modérateurs", color=discord.Color.red())
mention_error_embed = discord.Embed(title="❌ Erreur de Mention", description=" Veuillez mentionner 1 et 1 seule personne s'il vous plaît.", color=discord.Color.red())
#    discord.Embed(title="", description="", color="")


#mysql database


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ussent1001/rom34*",
  database="mydatabase"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE economie (idd BIGINT UNIQUE, argent INT, salaire INT)")
insord = "INSERT INTO economie VALUES (%s, %s, %s)"

#inventaire

mycursor.execute("CREATE TABLE meito (meitoID TINYINT NOT NULL AUTO_INCREMENT, nom TINYTEXT DEFAULT null, classe TINYTEXT, possesseur BIGINT UNIQUE DEFAULT null)")
for i in range(1, 84):
    if i < 51:
        cl = "Ryo Wazamono"
    elif i < 72:
        cl = "Ô Wazamono"
    else:
        cl = "Saijo Ô Wazamono"
    mycursor.execute("INSERT INTO meito (classe) VALUES (" + cl + ")")

#fdd

listeparamecia = {
"Ope Ope No Mi": None,
"Gomu Gomu No Mi": None,
"Bara Bara No Mi" : None,
"Sube Sube No Mi": None,
"Kilo Kilo No Mi": None,
"Bomu Bomu No Mi": None,
"Hana Hana No Mi": None,
"Doru Doru No Mi": None,
"Baku Baku No Mi": None,
"Mane Mane No Mi": None,
"Supa Supa No Mi": None,
"Toge Toge No Mi": None,
"Ori Ori No Mi": None,
"Bane Bane No Mi": None,
"Ito Ito No Mi": None,
"Noro Noro No Mi": None,
"Doa Doa No Mi": None,
"Awa Awa No Mi": None,
"Beri Beri No Mi": None,
"Sabi Sabi No Mi": None,
"Shari Shari No Mi": None,
"Yomi Yomi No Mi": None,
"Kage Kage No Mi": None,
"Horo Horo No Mi": None,
"Suke Suke No Mi": None,
"Nikyu Nikyu No Mi": None,
"Fruit De Jewerly Bonney": None,
"Jiki Jiki No Mi": None,
"Shiro Shiro No Mi": None,
"Fruit D'Urouge": None,
"Wara Wara No Mi": None,
"Oto Oto No Mi": None,
"Mero Mero No Mi": None,
"Doku Doku No Mi": None,
"Horu Horu No Mi": None,
"Choki Choki No Mi": None,
"Gura Gura No Mi": None,
"Kira Kira No Mi": None,
"Poke Poke No Mi": None,
"Woshu Woshu No Mi": None,
"Fuwa Fuwa No Mi": None,
"Fruit de Sanjuan Wolf": None,
"Gura Gura No Mi": None,
"Mato Mato No Mi": None,
"Fuku Fuku No Mi": None,
"Buki Buki No Mi": None,
"Guru Guru No Mi": None,
"Beta Beta No Mi": None,
"Zushi Zushi No Mi": None,
"Bari Bari No Mi": None,
"Nui Nui No Mi": None,
"Giro Giro No Mi": None,
"Ato Ato No Mi": None,
"Jake Jake No Mi": None,
"Pamu Pamu No Mi": None,
"Hobi Hobi No Mi": None,
"Sui Sui No Mi": None,
"Ton Ton No Mi": None,
"Hira Hira No Mi": None,
"Ishi Ishi No Mi": None,
"Fude Fude No Mi": None,
"Nagi Nagi No Mi": None,
"Chiyu Chiyu No Mi": None,
"Maki Maki No Mi": None,
"Soru Soru No Mi": None,
"Mira Mira No Mi": None,
"Pero Pero No Mi": None,
"Bisu Bisu No Mi": None,
"Kuri Kuri No Mi": None,
"Buku Buku No Mi": None,
"Bata Bata No Mi": None,
"Shibo Shibo No Mi": None,
"Memo Memo No Mi": None,
"Mochi Mochi No Mi": None,
"Hoya Hoya No Mi": None,
"Netsu Netsu No Mi": None,
"Kuku Kuku No Mi": None,
"Gocha Gocha No Mi": None,
"Kobu Kobu No Mi": None,
"Oshi Oshi No Mi": None,
"Toki Toki No Mi": None,
"Kibi Kibi No Mi": None,
"Suke Suke No Mi": None,
}
listezoan = {
"Ushi Ushi No Mi version Bison" : None ,
"Hito Hito No Mi" : None ,
"Tori Tori No Mi version Fauchon" : None ,
"Mogu Mogu No Mi" : None ,
"Inu Inu No Mi version Basset" : None ,
"Inu Inu No Mi version Chacal" : None ,
"Uma Uma No Mi" : None ,
"Neko Neko No Mi version Léopard" : None ,
"Zo Zo No Mi" : None ,
"Inu Inu No Mi version Loup" : None ,
"Ushi Ushi No Mi version Girafe" : None ,
"Hebi Hebi No Mi version Anaconda" : None ,
"Hebi Hebi No Mi version Cobra Royal" : None ,
"Kame Kame No Mi" : None ,
"Sara Sara No Mi version Axolotl" : None ,
"Mushi Mushi No Mi version Scarabée-Rhinocéros" : None ,
"Mushi Mushi No Mi version Guêpe" : None ,
"Tori Tori No Mi version Albatros" : None ,
"Inu Inu No Mi version Tanuki" : None , 
"Ryu Ryu No Mi version Allosaure" : None ,
"Zo Zo No Mi version Mammouth" : None ,
"Ryu Ryu No Mi version Spinosaure"  : None ,
"Ryu Ryu No Mi version Ptéranodon" : None ,
"Ryu Ryu No Mi version Brachiosaure" : None ,
"Ryu Ryu No Mi version Pachycephalosaure" : None ,
"Ryu Ryu No Mi version Tricératops" : None ,
"Kumo Kumo No Mi version Mygale" : None ,
"Kumo Kumo No Mi": None,
"Neko Neko No Mi version Tigre à dents de sabre" : None ,
"Tori Tori No Mi version Phoenix" : None ,
"Hito Hito No Mi version Bouddha" : None ,
"Uo Uo No Mi version Dragon Azur" : None ,
"Inu Inu No Mi version Renard à neuf queues" : None ,
"Hebi Hebi No Mi version Dragon à huit têtes" : None ,
"Inu Inu No Mi version Okuchi-no-Makami" : None ,
}
listelogia = {
"Moku Moku No Mi": None,
"Mera Mera No Mi": None,
"Suna Suna No Mi": None,
"Goro Goro No Mi": None,
"Hie Hie No Mi": None,
"Yami Yami No Mi": None,
"Pika Pika No Mi": None,
"Magu Magu No Mi": None,
"Numa Numa No Mi": None,
"Gasu Gasu No Mi": None,
"Yuki Yuki No Mi": None,
}
Lfdd = ['Ope Ope No Mi', 'Gomu Gomu No Mi', 'Bara Bara No Mi', 'Sube Suber No Mi', 'Kilo Kilo No Mi', 'Bomu Bomu No Mi', 'Hana Hana No Mi', 'Doru Doru No Mi', 'Baku Baku No Mi', 'Mane Mane No Mi', 'Supa Supa No Mi', 'Toge Toge No Mi', 'Ori Ori No Mi', 'Bane Bane No Mi', 'Ito Ito No Mi', 'Noro Noro No Mi', 'Doa Doa No Mi', 'Awa Awa No Mi', 'Beri Beri No Mi', 'Sabi Sabi No Mi', 'Shari Shari No Mi', 'Yomi Yomi No Mi', 'Kage Kage No Mi', 'Horo Horo No Mi', 'Suke Suke No Mi', 'Nikyu Nikyu No Mi', 'Fruit De Jewerly Bonney', 'Jiki Jiki No Mi', 'Shiro Shiro No Mi', "Fruit D'Urouge", 'Wara Wara No Mi', 'Oto Oto No Mi', 'Mero Mero No Mi', 'Doku Doku No Mi', 'Horu Horu No Mi', 'Choki Choki No Mi', 'Gura Gura No Mi', 'Kira Kira No Mi', 'Poke Poke No Mi', 'Woshu Woshu No Mi', 'Fuwa Fuwa No Mi', 'Fruit de Sanjuan Wolf', 'Mato Mato No Mi', 'Fuku Fuku No Mi', 'Buki Buki No Mi', 'Guru Guru No Mi', 'Beta Beta No Mi', 'Zushi Zushi No Mi', 'Bari Bari No Mi', 'Nui Nui No Mi', 'Giro Giro No Mi', 'Ato Ato No Mi', 'Jake Jake No Mi', 'Pamu Pamu No Mi', 'Hobi Hobi No Mi', 'Sui Sui No Mi', 'Ton Ton No Mi', 'Hira Hira No Mi', 'Ishi Ishi No Mi', 'Fude Fude No Mi', 'Nagi Nagi No Mi', 'Chiyu Chiyu No Mi', 'Maki Maki No Mi', 'Soru Soru No Mi', 'Mira Mira No Mi', 'Pero Pero No Mi', 'Bisu Bisu No Mi', 'Kuri Kuri No Mi', 'Buku Buku No Mi', 'Bata Bata No Mi', 'Shibo Shibo No Mi', 'Memo Memo No Mi', 'Mochi Mochi No Mi', 
'Hoya Hoya No Mi', 'Netsu Netsu No Mi', 'Kuku Kuku No Mi', 'Gocha Gocha No Mi', 'Kobu Kobu No Mi', 'Oshi Oshi No Mi', 'Toki Toki No Mi', 'Kibi Kibi No Mi', 'Ushi Ushi No Mi version Bison', 'Hito Hito no Mi', 'Tori Tori No Mi version Fauchon', 'Mogu Mogu No Mi', 'Inu Inu No Mi version Basset', 'Inu Inu No Mi version Chacal', 'Uma Uma No Mi', 'Neko Neko No Mi version Léopard', 'Zo Zo No Mi', 'Inu Inu No Mi version Loup', 'Ushi Ushi No Mi version Girafe', 'Hebi Hebi No Mi version Anaconda', 'Hebi Hebi No Mi version Cobra Royal', 'Kame Kame No Mi', 'Sara Sara No Mi version Axolotl', 'Mushi Mushi No Mi version Scarabée-Rhinocéros', 'Mushi Mushi No Mi version Guêpe', 'Tori Tori No Mi version Albatros', 'Inu Inu No Mi version Tanuki', 'Ryu Ryu No Mi version Allosaure', 'Zo Zo No Mi version Mammouth', 'Ryu Ryu No Mi version Spinosaure', 'Ryu Ryu No Mi version Ptéranodon', 'Ryu Ryu No Mi version Brachiosaure', 'Ryu Ryu No Mi version Pachycephalosaure', 'Ryu Ryu No Mi version Tricératops', 'Kumo Kumo No Mi version Mygale', 'Kumo Kumo No Mi', 'Neko Neko No Mi version Tigre à dents de sabre', 'Tori Tori No Mi version Phoenix', 'Hito Hito No Mi version Bouddha', 'Uo Uo No Mi version Dragon Azur', 'Inu Inu No Mi version Renard à neuf queues', 'Hebi Hebi No Mi version Dragon à huit têtes', 'Inu Inu No Mi version Okuchi-no-Makami', 'Moku Moku No Mi', 'Mera Mera No Mi', 'Suna Suna No Mi', 'Goro Goro No Mi', 'Hie Hie No Mi', 'Yami Yami No Mi', 'Pika Pika No Mi', 'Magu Magu No Mi', 'Numa Numa No Mi', 'Gasu Gasu No Mi', 'Yuki Yuki No Mi']

#opération sql

#mycursor.execute("CREATE TABLE fdd (nom TINYTEXT, type TINYTEXT, disponible BOOL DEFAULT 0, possesseur BIGINT DEFAULT null)")
#insertord = "INSERT INTO fdd (nom, type) VALUES (%s, %s)"
#for x in listeparamecia.keys():
#    Lis = [x, "paramecia"]
#    mycursor.execute(insertord, Lis)
#for x in listezoan.keys():
#    Lis = [x, "zoan"]
#    mycursor.execute(insertord, Lis)
#for x in listelogia.keys():
#    Lis = [x, "logia"]
#    mycursor.execute(insertord, Lis)
#mydb.commit()

#fonctions


class Economie(commands.Cog):
    @commands.command()
    async def Créditer(self, ctx):
        member = ctx.author.id
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        Brôles = ctx.guild.get_member(member).roles #B pour Brut 
        lrôles = [] 
        for i in Brôles: 
            lrôles.append(i.id)
        if 880495757604581417 in lrôles or 878962101903847445 in lrôles or 880486649191100477 in lrôles:
            a = ctx.message.mentions
            b = ctx.message.content
            b = b.split()
            c = b[-1]
            if len(a) != 1:
                await ctx.send(embed=mention_error_embed)
                return
            if len(b) != 3:
                await ctx.send(embed=discord.Embed(title="❌ Paramètre manquant", description="Vous avez oublier de préciser le montant à créditer.", color=discord.Color.red()))
                return
            if c.isnumeric() == False:
                if c[0] != "-" and c[:1].isnumeric() == False:
                    await ctx.send(embed=discord.Embed(title="❌ Paramètre défaillant", description="Veuillez préciser une somme entière de berrys à créditer", color=discord.Color.red()))
                    return
            c = int(c)
            idd = a[0].id
            mycursor.execute("SELECT idd FROM economie ")
            existe = mycursor.fetchall()
            Lexiste = []
            for x in range(0, len(existe)):
                y = existe[x]
                y = y[0]
                Lexiste.append(y)
            if idd not in Lexiste:
                insert = [idd, c, 0]
                mycursor.execute(insord, insert)
                avant = 0
                après = c
            else:
                mycursor.execute("SELECT argent FROM economie WHERE idd = " + str(idd))
                show = mycursor.fetchone()
                avant = show[0]
                après = c + avant
                mycursor.execute("UPDATE economie SET argent = " + str(après) + " WHERE idd = " + str(idd))
            mydb.commit()
            moneymsg = "La créditation a bien été effectuée! \n Avant: " + str(avant)
            moneymsg = moneymsg + "<:berry:903741046255665263>\n Après: " + str(après) + "<:berry:903741046255665263>"
            await ctx.send(embed=discord.Embed(title="💳 Créditation effectuée", description=moneymsg, color=discord.Color.blue()))
        else:
            await ctx.send(embed=admin_error_embed)
            return

    @commands.command()
    async def fdd(self, ctx):
        idd = ctx.message.author.id
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        contenu = str(ctx.message.content).split()
        if contenu[1] == "chercher":
            #?fdd chercher Ope Ope no Mi
            contenu = str(ctx.message.content)[14:]
            if contenu not in Lfdd:
                d = "Désolé mais le fruit du démon que vous avez essayé de chercher (**" + contenu + "**) est introuvable."
                await ctx.send(embed=discord.Embed(title="❌ FDD Introuvable", description=d, color=discord.Color.red()))
                return
            mycursor.execute("SELECT disponible, possesseur FROM fdd WHERE nom = '" + contenu + "'")
            a = mycursor.fetchone() #0 ou 1
            if a[0] == 0 and a[1] == None:
                d = " Le **" + contenu + "** est actuellement disponible!"
                await ctx.send(embed=discord.Embed(title="🍈 FDD Disponible", description=d, color=discord.Color.green()))
                return
            else:
                if a[0] == 1:
                    d = "Désolé mais le **" + contenu + "** est réservé pour un event."
                    await ctx.send(embed=discord.Embed(title="🔐 FDD Réservé", description=d, color=discord.Color.orange()))
                    return
                idd = a[1]
                try:
                    d = "Désolé mais le **" + contenu + "** est possédé par **" + ctx.guild.get_member(idd).name + "#" + ctx.guild.get_member(idd).discriminator + "**."
                    await ctx.send(d)
                    return
                except:
                    d = """Il semblerait que la personne qui possède ce fruit ait quitté le serveur. Il est peut-être disponible (voir avec le staff)
                    ID du RPlayer qui a quitté: """ + str(idd)
                    await ctx.send(embed=discord.Embed(title="❓ FDD contesté", description=d, color=discord.Color.purple()))
        if contenu[1] == "donner":
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
            if len(ctx.message.mentions) == 0:
                if contenu[2].isnumeric() == True:
                    chercher = int(contenu[2])
                    contenu = ctx.message.content[31:]
                    if ctx.guild.get_member(chercher) == None:
                        d = "Désolé mais l'ID que vous avez inséré est invalide (**" + str(chercher) + "**). \n Vérifiez si vous avez bien inséré l'ID et si le membre est présent sur ce serveur."
                        await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description=d, color=discord.Color.red()))
                        return
                else:
                    await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il y a une erreur dans votre commande.\n Vérifiez bien si vous avez mentionné quelqu'un / inséré un ID valide."), color=discord.Color.red())
                    return
            else:
                if ctx.message.mentions[0].id != None:
                    chercher = ctx.message.mentions[0].id
                    contenu = ctx.message.content[35:]
                else:
                    await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Il y a une erreur dans votre commande.\n Vérifiez bien si vous avez mentionné quelqu'un / inséré un ID valide."), color=discord.Color.red())
                    return
                if ctx.guild.get_member(chercher) == None:
                    d = "Désolé mais l'ID que vous avez inséré / la personne que vous avez mentionné est invalide (**ID : " + str(chercher) + "**). \n Vérifiez si vous avez bien inséré l'ID et si le membre est présent sur ce serveur."
                    await ctx.send(embed=discord.Embed(title="❌ Membre Introuvable", description=d, color=discord.Color.red()))
                    return
            if contenu not in Lfdd:
                d = "Désolé mais le fruit du démon que vous avez essayé de donner (**" + contenu + "**) est introuvable."
                await ctx.send(embed=discord.Embed(title="❌ FDD Introuvable", description=d, color=discord.Color.red()))
                return
            mycursor.execute("UPDATE fdd SET possesseur = " + str(chercher) + " WHERE nom = '" + contenu + "'")
            mydb.commit()
            d = "Le **" + contenu + "** a été donné avec succès à " + ctx.guild.get_member(chercher).mention + "!"
            await ctx.send(embed=discord.Embed(title="✅ FDD Donné", description=d, color=discord.Color.blue()))
            return
        if contenu[1] == "retirer":
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
            contenu = str(ctx.message.content)[13:]
            if contenu not in Lfdd:
                d = "Désolé mais le fruit du démon que vous avez essayé de retirer à quelqu'un / retirer la réservation (**" + contenu + "**) est introuvable."
                await ctx.send(embed=discord.Embed(title="❌ FDD Introuvable", description=d, color=discord.Color.red()))
                return
            mycursor.execute("SELECT possesseur FROM fdd WHERE nom = '" + contenu + "'")
            idd = mycursor.fetchone()[0]
            mycursor.execute("SELECT disponible FROM fdd WHERE nom = '" + contenu + "'")
            nlibre = mycursor.fetchone()[0]
            if idd == None and nlibre == False:
                d = "Le **" + contenu + "** est déjà disponible!"
                await ctx.send(embed=discord.Embed(title="🍈 FDD Disponible", description=d, color=discord.Color.orange()))
                return
            elif idd == None and nlibre == True:
                mycursor.execute("UPDATE fdd SET disponible = 0 WHERE nom = '" + contenu + "'")
                mydb.commit()
                d = "Le **" + contenu + "** est maintenant disponible! (anciennement réservé)"
                await ctx.send(embed=discord.Embed(title="♻️ Fruit Libéré", description=d, color=discord.Color.green()))
                return
            else: 
                mycursor.execute("UPDATE fdd SET possesseur = null WHERE nom = '" + contenu + "'")
                mycursor.execute("UPDATE fdd SET disponible = 0 WHERE nom = '" + contenu + "'")
                mydb.commit()
                d = "Le **" + contenu + "** (anciennement possédé par une personne ayant comme ID:** " + str(idd) + "**) est maintenant disponible!"
                await ctx.send(embed=discord.Embed(title="♻️ Fruit Libéré", description=d, color=discord.Color.green()))
                return
        if contenu[1] == "réserver":
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
            contenu = str(ctx.message.content)[14:]
            if contenu not in Lfdd:
                d = "Désolé mais le fruit du démon que vous avez essayé de retirer à quelqu'un / nettoyer (**" + contenu + "**) est introuvable."
                await ctx.send(embed=discord.Embed(title="❌ FDD Introuvable", description=d, color=discord.Color.red()))
                return
            mycursor.execute("SELECT disponible FROM fdd WHERE nom = '" + contenu + "'")
            res = mycursor.fetchone()[0]
            if res == 0:
                mycursor.execute("UPDATE fdd SET disponible = 1 WHERE nom = '" + contenu + "'")
                mydb.commit()
                d = "Le **" + contenu + "** a été réservé avec succès!"
                await ctx.send(embed=discord.Embed(title="🔐 FDD Réservé", description=d, color=discord.Color.green()))
                return
            else:
                d = "Le **" + contenu + "** est déjà réservé!"
                await ctx.send(embed=discord.Embed(title="🔐 FDD Déjà Réservé", description=d, color=discord.Color.orange()))
                return
        if contenu[1] == "nettoyer":
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
            mycursor.execute("SELECT possesseur FROM fdd")
            Lfddbrut = mycursor.fetchall()
            LRPfdd = []
            position = 0
            for x in Lfddbrut:
                y = Lfddbrut[position]
                position+=1
                if y[0] != None:
                    LRPfdd.append(y[0])
            fddl = []
            apos = []
            for RPlayer in LRPfdd:
                if ctx.guild.get_member(RPlayer) == None:
                    mycursor.execute("SELECT nom FROM fdd WHERE possesseur = " + str(RPlayer))
                    a = mycursor.fetchall()
                    mycursor.execute("UPDATE fdd SET possesseur = null WHERE possesseur = " + str(RPlayer))
                    if len(a) > 1:
                        for b in a:
                            print(b)
                            fddl.append(b[0])
                            apos.append(RPlayer)
                    elif len(a) == 1:
                        b = a[0]
                        fddl.append(b[0])
                        apos.append(RPlayer)
            mydb.commit()
            if len(apos) == 0:
                await ctx.send(embed=discord.Embed(title="✅ Rien à Nettoyer", description="Il n'y a aucun fruit à nettoyer!", color=discord.Color.green()))
                return
            else:
                m = "Voici les fruits du démon qui ont été nettoyés: \n"
                for x in range(0, len(fddl)):
                    m = m + str(x+1) + ") **" + fddl[x] + "** (anciennement possédé par une personne ayant comme ID: **" + str(apos[x]) + "**).\n"
                await ctx.send(embed=discord.Embed(title="♻️ Nettoyage Effectué", description=m, color=discord.Color.orange()))
                return 

    @commands.command()
    async def meito(self, ctx):
        if ctx.guild.id != 878962067309199410 and ctx.guild.id != 700641156643553301: #op, testzone
            await ctx.send(embed=discord.Embed(title="⛔ Commande Interdite sur le Serveur", description="Désolé mais cette commande est interdite sur ce serveur.", color=discord.Color.red()))
            return
        contenu = str(ctx.message.content).split()
        idd = ctx.author.id
        if contenu[1] == "renommer":
            mycursor.execute("SELECT possesseur FROM meito WHERE possesseur = " + str(idd))
            a = mycursor.fetchone()
            if a == []:
                await ctx.send(embed=discord.Embed(title="❌ Meito Introuvable", description="Désolé mais il semblerait que vous ne possédez aucune Meito. Par conséquent, vous ne pouvez pas renommer votre Meito puisque vous n'en avez aucune.", color=discord.Color.red()))
                return
            else:
                nom = str(ctx.message.content)[15:]
                print(nom)
                mycursor.execute("SELECT nom FROM meito WHERE possesseur = " + str(idd))
                a = mycursor.fetchone()[0]
                if a == None:
                    bo = "Aucun"
                else:
                    bo = a
                mycursor.execute("SELECT classe FROM meito WHERE possesseur = " + str(idd))
                a = mycursor.fetchone()[0]
                mycursor.execute("UPDATE meito SET nom = '" + nom + "' WHERE possesseur = " + str(idd))
                mydb.commit()
                d = "Le nom de votre Meito (classe **" + a +  "**) a été changé avec succès!\n Ancien nom: :dagger: **" + bo + "** :dagger:\n Nouveau nom: :dagger: **" + nom + "** :dagger:"
                await ctx.send(embed=discord.Embed(title="✒️ Changement de Nom effectué", description=d, color=discord.Color.green()))
                return
        elif contenu[1] == "donner":
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
            if len(message) != 4:
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
            rroles = ctx.guild.get_member(idd).roles
            Lroles = []
            for r in rroles:
                Lroles.append(r.id())
            if 880538065414811668 not in Lroles:
                await ctx.send(embed=discord.Embed(title="❌ Rôle Manquant", description="Désolé mais la personne que vous avez mentionné n'a pas le rôle sabreur. Par conséquent, elle ne peut pas recevoir de meito.", color=discord.Color.green()))
                return
            if message[3] == "Ryo":
                cla = "Ryo Wazamono"
            elif message[3] == "Ô" or message[3] == "O":
                cla = "Ô Wazamono"
            elif message[3] == "Saijo" or message[3] == "Saijô":
                cla = "Saijo Ô Wazamono"
            else:
                await ctx.send(embed=discord.Embed(title="❌ Mauvaise Classe", description="Désolé mais la sous-classe que vous avez inséré est invalide.\n Veuillez en choisir une parmis:\n Ryo | Ô | Saijo (sans rajouter Wazamono à la fin).", color=discord.Color.red()))
                return
            mycursor.execute("SELECT meitoID FROM meito WHERE classe = '" + cla + "'")
            a = mycursor.fetchall()
            fin = False
            for i in a:
                mycursor.execute("SELECT possesseur FROM meito WHERE meitoID = " + str(i[0]))
                a = mycursor.fetchone()[0]
                if a == None:
                    mycursor.execute("UPDATE meito SET possesseur = " + str(idd) + " WHERE meitoID = " + str(i[0]))
                    mydb.commit()
                    fin = True
                    break
            if fin == False:
                ti = "❌ Aucune " + cla + " disponible."
                await ctx.send(embed=discord.Embed(title=ti, description="Désolé mais aucune meito de cette classe n'est disponible.", color=discord.Color.red()))
            else:
                d = "La **" + cla + "** a été donnée avec succès à " + ctx.guild.get_member(idd).mention
                await ctx.send(embed=discord.Embed(title="✅ Meito Donnée", description="La meito a été donnée avec succès "))
            return
        elif contenu[1] == "nettoyer":
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
            mycursor.execute("SELECT possesseur FROM meito")
            a = mycursor.fetchall()
            Lpos = []
            Lsup = []
            for i in a:
                if i[0] == None:
                    continue
                Lpos.append(i[0])
            for RP in Lpos:
                if ctx.guild.get_member(RP) == None:
                    Lsup.append(RP)
            if Lsup == []:
                await ctx.send(embed=discord.Embed(title="✅ Aucune Meito à Nettoyer", description="Il n'y a aucune meito à nettoyer.", color=discord.Color.green()))    
            else:
                ryo = 0
                o = 0
                saijo = 0
                for i in Lsup:
                    mycursor.execute("SELECT classe FROM meito WHERE posesseur = " + str(i))
                    a = mycursor.fetchone()[0]
                    if a == "Ryo Wazamono":
                        ryo += 1
                    elif a == "Ô Wazamono":
                        o += 1
                    else:
                        saijo += 1
                    mycursor.execute("UPDATE meito SET possesseur = null WHERE possesseur = " + str(i))
                mydb.commit()
                if ryo == 0:
                    sryo = ""
                elif ryo == 1:
                    sryo = "\n- **1** Ryo Wazamono a été libérée."
                else:
                    sryo = "\n- **" + str(ryo) + "** Ryos Wazamono ont été libérées."
                if o == 0:
                    so = ""
                elif o == 1:
                    so = "\n- **1** Ô Wazamono a été libérée."
                else:
                    so = "\n- **" + str(o) + "** Ô Wazamono ont été libérées."
                if saijo == 0:
                    ssaijo = ""
                elif saijo == 1:
                    ssaijo = "\n- **1** Saijo Ô Wazamono a été libérée."
                else:
                    ssaijo = "\n- **" + str(saijo) + "** Saijo Ô Wazamono ont été libérées."
                d = "La liste des Meitos a été nettoyé avec succès!" + sryo + so + ssaijo
                await ctx.send(embed=discord.Embed(title="♻️ Meitos Nettoyées", description=d, color=discord.Color.green()))
            return
        elif contenu[1] == "retirer":
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
            mycursor.execute("SELECT possesseur FROM meito")
            a = mycursor.fetchall()
            Lpos = []
            Lsup = []
            for i in a:
                if i[0] == None:
                    continue
                Lpos.append(i[0])
            if idd not in Lpos:
                await ctx.send(embed=discord.Embed(title="✅ Membre sans Meito", description="Le membre que vous avez mentionné n'a pas de meito. Par conséquent, je ne peux pas lui retirer sa meito s'il n'en possède pas.", color=discord.Color.green()))
            else:
                mycursor.execute("UPDATE meito SET possesseur = null WHERE possesseur = " + str(idd))
                mydb.commit()
                await ctx.send(embed=discord.Embed(title="♻️ Meito Retirée avec succès.", description="La meito de cette personne a été retirée avec succès.", color=discord.Color.green()))
            return
        else:
            await ctx.send(embed=discord.Embed(title="❌ Mauvaise Commande", description="Désolé mais le paramètre définissant la sous-commande à exécuter est invalide. Veuillez en choisir un parmis:\n renommer | donner | nettoyer | retirer | chercher .", color=discord.Color.red()))
            return
def setup(client):
    client.add_cog(Economie(client))