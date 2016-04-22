# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para StreamSports
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os, re, xbmc
from core import scrapertools
from core import logger
from core import config
from core.item import Item
from core.scrapertools import decodeHtmlentities as dhe

__channel__ = "streamsports"
__category__ = "d"
__type__ = "generic"
__title__ = "StreamSports"
__language__ = "ES"

host ="http://www.streamsports.me"
song = os.path.join(config.get_runtime_path(), 'queen-we-will-rock-you.mp3')
DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.streamsports mainlist")
    itemlist = []

    check =xbmc.getInfoLabel('Container.FolderPath')
    if "deportes" in check:
        xbmc.executebuiltin('xbmc.PlayMedia('+song+')')

    itemlist.append(Item(channel=__channel__, title="Agenda/Directos", action="entradas", url=host, thumbnail="http://i.imgur.com/3J5DbZA.png?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="Fútbol", action="entradas", url=host+"/football/", thumbnail="http://i.imgur.com/3J5DbZA.png?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="Baloncesto", action="entradas", url=host+"/basketball/", thumbnail="http://i.imgur.com/3J5DbZA.png?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="Más Deportes", action="categorias", url=host, thumbnail="http://i.imgur.com/3J5DbZA.png?1", folder=True))

    return itemlist

def categorias(item):
    logger.info("pelisalacarta.channels.streamsports categorias")
    itemlist = []
    itemlist.append(Item(channel=__channel__, title="Fútbol Americano", action="entradas", url=host+"/americanfootball/", thumbnail=item.thumbnail, folder=True))

    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    bloque = scrapertools.find_single_match(data, "<ul class='dropdown-menu'>(.*?)</ul>")
    patron = '<a href="([^"]+)">.*?alt="([^"]+)"' 
    matches = scrapertools.find_multiple_matches(bloque, patron)
    sports = {'Baseball':'Béisbol', 'Tennis':'Tenis', 'Boxing':'Boxeo',
              'Cycling':'Ciclismo', 'Motorsports':'Motor', 'Athletics':'Atletismo'}

    for scrapedurl, scrapedtitle  in matches:
        if scrapedtitle in sports:
            scrapedtitle = scrapedtitle.replace(scrapedtitle, sports[scrapedtitle])
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="entradas", url=host+scrapedurl, thumbnail=item.thumbnail, folder=True))

    itemlist.sort(key=lambda item: item.title)
    return itemlist

def entradas(item):
    logger.info("pelisalacarta.channels.streamsports entradas")
    itemlist = []
    sports = {'Football':'Fútbol','Baseball':'Béisbol', 'Tennis':'Tenis', 'Boxing':'Boxeo', 'American Football':'Fútbol Americano',
              'Basketball':'Baloncesto','Cycling':'Ciclismo', 'Motorsports':'Motor', 'Athletics':'Atletismo'}

    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    data = dhe(data)

    bloque = scrapertools.find_single_match(data, '<tbody>(.*?)</tbody>')
    patron = '<tr>.*?<span>([A-z]+)(\d+)</span>.*?<span class=\'(timepast|time)\'>' \
             '<span class="hours">(.*?)</span>(.*?)</span>' \
             '.*?</br>(.*?)</td>.*?</span>.*?alt="([^"]+)"' \
             '.*?<strong>(.*?)</strong>.*?<strong>(.*?)</strong>' \
             '.*?href="([^"]+)"'
    matches = scrapertools.find_multiple_matches(bloque, patron)

    for mes, dia, live, hora, minutos, deporte, torneo, equipo1, equipo2, scrapedurl  in matches:
        from time import strptime
        mes = str(strptime(mes,'%b').tm_mon)
        hora = str(int(hora)+1) if int(hora) < 23 else "0"
        fecha = "["+dia+"/"+mes+"] "

        if live == "timepast": scrapedtitle = "[COLOR red][B]"+fecha+hora+minutos+"[/B][/COLOR]"
        else: scrapedtitle = "[COLOR green][B]"+fecha+hora+minutos+"[/B][/COLOR]"
        if (equipo1 or equipo2) != "N/A":
            partido = " [COLOR darkorange][B]"+equipo1+" vs "+equipo2+"[/B][/COLOR]"
            scrapedtitle += partido
        else: partido = ""

        if deporte in sports: deporte = deporte.replace(deporte, sports[deporte])
        if item.url == host:
            scrapedtitle += " [COLOR blue]("+deporte+"-"+torneo+")[/COLOR]"
        else:
            scrapedtitle += " [COLOR blue]("+torneo+")[/COLOR]"
        
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, action="findvideos", url=host+scrapedurl, thumbnail=item.thumbnail, fulltitle=scrapedtitle, match=partido, competicion=deporte+"-"+torneo, folder=True) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.streamsports play")
    itemlist = []
    if item.match == "": item.match = "[COLOR darkorange]"+item.competicion+"[/COLOR]"

    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    bloque = scrapertools.find_single_match(data, '<h4 class="streamTypes" id="p2p">(.*?)</table>')

    if bloque != "":
        bloques = scrapertools.find_multiple_matches(bloque, '(<td>[^<]+<span style="font-size:10px">.*?</span></span></td>)')
        for match in bloques:
            patron = '<td>(.*?)<.*?<td>(.*?)<.*?<td>(.*?)<.*?<a href="([^"]+)"'
            matches = scrapertools.find_multiple_matches(match, patron)
            for bitrate, server, idioma, scrapedurl in matches:
                if not scrapedurl.startswith("acestream") and not scrapedurl.startswith("sop"): continue
                server = "[COLOR blue]"+server.strip()+"[/COLOR] "
                bitrate = " [COLOR green]("+bitrate.strip()+")[/COLOR]"
                idioma = " [COLOR gold]("+idioma.strip()+")[/COLOR]"
                scrapedtitle = server + item.match + bitrate + idioma
                scrapedurl= scrapedurl + "|" + item.match
        
                itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", idioma=idioma, thumbnail=item.thumbnail, folder=False))
        itemlist.sort(key=lambda item: item.idioma, reverse=True)

    if "No Sopcast/Acestream streams added yet" in data or len(itemlist) == 0:
        itemlist.append(Item(channel=__channel__, title="[COLOR yellow]No hay enlaces disponibles. Inténtalo más tarde[/COLOR]", url="", action="", thumbnail=item.thumbnail, folder=False))

    return itemlist


def play(item):
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    itemlist = []
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=item.url, action="play", folder=False))

    return itemlist
