# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para MotoGPEnNegro
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "motogpennegro"
__type__ = "generic"
__title__ = "MotoGPEnNegro"
__language__ = "ES"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.motogpennegro mainlist")
    itemlist = []

    data = scrapertools.cachePage("https://motogpennegro.wordpress.com/streaming/")
    patron = '<a href="(http://adf.ly/[^"]+)".*?src="(.*?(?:jpg|png)).*?alt="([^"]+)"'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedthumbnail, tipo in matches:
        if tipo == "MotoGP-Logo": continue
        elif "MotoGP" in tipo:
            title = "[COLOR darkred]Canal Moto GP (Acestream)[/COLOR]"
            fanart = "http://i.imgur.com/eN4utvy.jpg?1"
        elif "formula" in tipo: 
            title = "[COLOR darkcyan]Canal Formula 1 (Acestream)[/COLOR]"
            fanart = "http://i.imgur.com/pdnifhG.jpg?1"
        itemlist.append(Item(channel=__channel__, title=title, url=scrapedurl, action="play", thumbnail=scrapedthumbnail, fanart=fanart))
    itemlist.append(Item(channel=__channel__, title="[COLOR sienna]Hemeroteca (Solo 1fichier)[/COLOR]", url="", action="hemeroteca", thumbnail="http://i.imgur.com/LjJu39J.png?1", fanart="http://i.imgur.com/eN4utvy.jpg?1"))

    return itemlist


def hemeroteca(item):
    logger.info("pelisalacarta.channels.motogpennegro hemeroteca")
    itemlist = []

    title = "[COLOR goldenrod]%s[/COLOR]"
    itemlist.append(Item(channel=__channel__, title=title % "Temporada 2016", url="https://motogpennegro.wordpress.com/", action="menu_heme", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    itemlist.append(Item(channel=__channel__, title=title % "Temporada 2013", url="https://1fichier.com/dir/EW6eYIUF", action="findvideos", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    itemlist.append(Item(channel=__channel__, title=title % "Temporada 2010", url="https://1fichier.com/dir/r1qZyW62", action="findvideos", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    itemlist.append(Item(channel=__channel__, title=title % "Documentales", url="https://1fichier.com/dir/gDKDZGYg", action="findvideos", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    itemlist.append(Item(channel=__channel__, title=title % "Extras", url="https://1fichier.com/dir/6B01q5z2", action="findvideos", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))

    return itemlist


def menu_heme(item):
    logger.info("pelisalacarta.channels.motogpennegro menu_heme")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    title = scrapertools.find_single_match(item.title, '\]([^\[]+)\[')
    bloque = scrapertools.find_single_match(data, title.upper() + "</a><ul(.*?)</ul>")
    matches = scrapertools.find_multiple_matches(bloque, '<a href="([^"]+)">(.*?)</a>')
    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = "[COLOR orangered]"+scrapertools.decodeHtmlentities(scrapedtitle)+"[/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="carreras", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    
    return itemlist


def carreras(item):
    logger.info("pelisalacarta.channels.motogpennegro carreras")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    patron = '<h2 style="text-align:center;">(.*?)</h2>.*?src="([^"]+)".*?<a href="([^"]+)"'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedtitle, scrapedthumbnail, scrapedurl in matches:
        scrapedtitle = "[COLOR green]Ver Carrera de[/COLOR] [COLOR darkorange]"+scrapedtitle+"   [1fichier][/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", thumbnail=scrapedthumbnail, fanart=item.fanart, folder=False))
    
    itemlist.sort(reverse=True)
    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.channels.motogpennegro findvideos")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    patron = '<tr>.*?<a href="([^"]+)".*?>(.*?)</a>.*?<td class="normal">(.*?)</td>'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedtitle, size in matches:
        scrapedtitle = "[COLOR sienna]"+scrapedtitle+"[/COLOR]  [COLOR orangered]("+size+")   [1fichier][/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", thumbnail=item.thumbnail, fanart=item.fanart, folder=False))
    return itemlist
    
    
def play(item):
    logger.info("pelisalacarta.channels.motogpennegro play")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    if "Acestream" in item.title:
        decoded_url = decode_adfly(data)
        url = "acestream://" + decoded_url.rsplit("/",1)[1]
        itemlist.append(Item(channel=__channel__, title=item.title, action="play", server="p2p", url=url, thumbnail=item.thumbnail, folder=False))
    elif "1fichier" in item.url:
        itemlist.append(Item(channel=__channel__, title=item.title, action="play", server="onefichier", url=item.url, thumbnail=item.thumbnail, folder=False))
    else:
        url = decode_adfly(data)
        itemlist.append(Item(channel=__channel__, title=item.title, action="play", server="onefichier", url=url, thumbnail=item.thumbnail, folder=False))
    return itemlist


def decode_adfly(data):
    import base64
    ysmm = scrapertools.find_single_match(data, "var ysmm = '([^']+)'")
    left = ''
    right = ''
    for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
        left += c[0]
        right = c[1] + right

    decoded_url = base64.b64decode(left.encode() + right.encode())[2:].decode()
    return decoded_url
