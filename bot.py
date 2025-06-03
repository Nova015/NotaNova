import discord
import os
import pytz
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext import commands
import asyncio

load_dotenv()
#TOKEN del bot
TOKEN = os.getenv("TOKEN")
ID_ASISTENCIA=1098776649060864051
ID_UPDATE=1073289305662967940

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents)
#scheduler = AsyncIOScheduler()
#Activar en servidor
scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Mexico_City'))

#Funcion de programacion de tareas (envio de recordatorios)
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

    if not scheduler.running:
        scheduler.add_job(enviar_recordatorios, 'cron', day_of_week='thu', hour=12, minute=0)
        scheduler.add_job(avance_urgente, 'cron', day_of_week='thu', hour=16, minute=0)
        scheduler.start()

#funcion que obtner el contenido de los mensajes ubicados en la carpeta de recordatorios.
def cargar_mensaje(nombre_archivo):
    ruta_completa = os.path.join("recordatorios", nombre_archivo)
    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        return archivo.read()
    

#Funcion que envia los recordatorios de entrega de avance y asistencia a junta semanal.
async def enviar_recordatorios():
    print("¡Recordatorio programado ejecutado!") 
    canal_asistencia = bot.get_channel(ID_ASISTENCIA)
    canal_update = bot.get_channel(ID_UPDATE)

    mensaje_avance = cargar_mensaje("mensaje_avance.txt")

    with open("recordatorios/JuntaSemanal.png", "rb") as f:
        picture = discord.File(f)
    link_asistencia = cargar_mensaje("asistenciaJunta.txt")

    if canal_asistencia:
        await canal_asistencia.send(mensaje_avance)
    if canal_update:
        mensajePrincipal=await canal_update.send("@everyone", file=picture)
        mensajeReg = f"Registra tu asistencia: [Aquí]({link_asistencia})"
        await mensajePrincipal.reply(mensajeReg)

#Funcion que envia el recordatorio de entrega de avance semanal una hora antes de su vencimiento
async def avance_urgente():
    canal_asistencia = bot.get_channel(ID_ASISTENCIA)
    mensaje_urgente = cargar_mensaje("mensaje_avanceUrgente.txt")
    await canal_asistencia.send(mensaje_urgente)

#Funcion para el envio de mensajes personalizados a nuevos integrantes
# @bot.event
# async def on_member_join(member):
#     try:
#         mensaje_bienvenida=cargar_mensaje("mensaje_bienvenida.txt")
#         mensaje_per=mensaje_bienvenida.format(
#             usuario=member.name,
#             id_asistencia=ID_ASISTENCIA
#         )

#         await member.send(mensaje_per)
#         print(f"Mensaje enviado a {member.name}")
#     except discord.Forbidden:
#         print(f"No se pudo enviar DM a {member.name} (DMs desactivados).")

#comando !testdm para realizacion de pruebas (envio de DM a usuarios)
#NOTA: si ya no es necesario realizar pruebas, la funcion se puede eliminar
@bot.command()
async def testdm(ctx):
    try:
        await ctx.author.send("¡Esto es una prueba de mensaje directo!")
    except discord.Forbidden:
        await ctx.send("No pude enviarte un DM. ¿Tienes los mensajes privados activados?")

#comando !testprueba para realizar pruebas de envio de recordatorios (los mensajes se envian a los canales al momento en que se ejcute este comando)
#Esta funcion se puede eliminar en caso de no requerir hacer pruebas.
@bot.command()
async def testprueba(ctx):
    await ctx.send("Eviando mensajes de prueba")
    await enviar_recordatorios()

@bot.command()
async def contactosAdmin(ctx):
    mensaje_contacto = cargar_mensaje("contactos_admin.txt")
    await ctx.send(mensaje_contacto)

bot.run(TOKEN)
#client.run(TOKEN)

