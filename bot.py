import discord
import os
import pytz
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext import commands
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
ID_ASISTENCIA=1098776649060864051
ID_UPDATE=1073289305662967940

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents)
scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Mexico_City'))

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

    if not scheduler.running:
        scheduler.add_job(enviar_recordatorios, 'cron', day_of_week='thu', hour=7, minute=0)
        scheduler.add_job(avance_urgente, 'cron', day_of_week='thu', hour=16, minute=0)
        scheduler.start()


def cargar_mensaje(nombre_archivo):
    ruta_completa = os.path.join("recordatorios", nombre_archivo)
    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        return archivo.read()

async def enviar_recordatorios():
    print("¡Recordatorio programado ejecutado!") 
    canal_asistencia = bot.get_channel(ID_ASISTENCIA)
    canal_update = bot.get_channel(ID_UPDATE)

    mensaje_avance = cargar_mensaje("mensaje_avance.txt")
    mensaje_junta = cargar_mensaje("mensaje_junta.txt")
    link_asistencia = cargar_mensaje("asistenciaJunta.txt")

    if canal_asistencia:
        await canal_asistencia.send(mensaje_avance)
    if canal_update:
        mensajePrincipal=await canal_update.send(mensaje_junta)
        await mensajePrincipal.reply(link_asistencia)

async def avance_urgente():
    canal_asistencia = bot.get_channel(ID_ASISTENCIA)
    mensaje_urgente = cargar_mensaje("mensaje_avanceUrgente.txt")
    await canal_asistencia.send(mensaje_urgente)

@bot.command()
async def testbot(ctx):
    await ctx.send("Eviando mensajes de prueba")
    await enviar_recordatorios()
bot.run(TOKEN)
#client.run(TOKEN)

