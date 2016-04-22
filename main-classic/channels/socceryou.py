# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para SoccerYou
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "socceryou"
__type__ = "generic"
__title__ = "SoccerYou"
__language__ = "ES"

DEBUG = config.get_setting("debug")
host_soccer = "http://www.socceryou.com/es/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.socceryou mainlist")
    itemlist = []

    itemlist.append(Item(channel=__channel__, title="Últimos partidos", url="http://www.socceryou.com/es/partidos-completos.php", action="novedades", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Últimos resúmenes", url="http://www.socceryou.com/es/resumenes.php", action="novedades", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Programas", url="http://www.socceryou.com/es/programastv.php", action="novedades", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Competiciones", url="http://www.socceryou.com/es/partidos-completos.php", action="competiciones", thumbnail=item.thumbnail, fanart=item.fanart))

    return itemlist

def novedades(item):
    logger.info("pelisalacarta.channels.socceryou novedades")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    patron = '<div class="foto-video">.*?title="([^"]+)"><a href ="([^"]+)"' \
             '.*?(?:src=|src =)"([^"]+)".*?<span class="fecha-video">(.*?)</span>'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedtitle, scrapedurl, scrapedthumbnail, fecha in matches:
        scrapedtitle = "[COLOR indianred]"+scrapertools.entitiesfix(scrapedtitle).replace("&nbsp"," ")+"[/COLOR]"
        scrapedtitle += " [COLOR darkorange]("+fecha.replace("Played: ","")+")[/COLOR]"
        if "no-thumbnail.jpg" in scrapedthumbnail: scrapedthumbnail = item.thumbnail
        elif scrapedthumbnail.startswith("//"): scrapedthumbnail = "http:"+scrapedthumbnail
        else: scrapedthumbnail = "http://www.socceryou.com"+scrapedthumbnail
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html(scrapedtitle), action="findvideos", url=host_soccer+scrapedurl, thumbnail=scrapedthumbnail, folder=True))

    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)">Siguiente</a>')
    if next_page != "":
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", action="novedades", url=item.url+next_page, thumbnail=item.thumbnail, folder=True))

    return itemlist

def competiciones(item):
    logger.info("pelisalacarta.channels.socceryou competiciones")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    bloque = scrapertools.find_single_match(data, '<ul class="nav-sub2">(.*?)</ul>')
    matches = scrapertools.find_multiple_matches(bloque, '<a href ="([^"]+)".*?</span>(.*?)</li>')
    for scrapedurl, scrapedtitle in matches:
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="menu", url=host_soccer+scrapedurl, thumbnail=item.thumbnail, folder=True))

    itemlist.append(Item(channel=__channel__, title="Todas las Competiciones", action="menu", url="http://www.socceryou.com/es/competiciones.php", thumbnail=item.thumbnail, folder=True))

    return itemlist

def menu(item):
    logger.info("pelisalacarta.channels.socceryou menu")
    itemlist = []
    if item.title == "Todas las Competiciones":
        data = scrapertools.cachePage(item.url)
        data = data.replace("\n","").replace("\t","")
        bloque = scrapertools.find_single_match(data, '<ul class="todos-equipos">(.*?)</ul>')
        matches = scrapertools.find_multiple_matches(bloque, 'src ="([^"]+)".*?<a href ="([^"]+)">(.*?)</a>')
        for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
            scrapedthumbnail = "http://www.socceryou.com"+scrapedthumbnail
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="menu", url=host_soccer+scrapedurl, thumbnail=scrapedthumbnail, folder=True))
    else:
        scrapedurl = item.url.replace("proximos-encuentros","partidos-completos")
        itemlist.append(Item(channel=__channel__, title="Partidos Completos", action="novedades", url=scrapedurl, thumbnail=item.thumbnail, folder=True))
        scrapedurl = item.url.replace("proximos-encuentros","resumenes")
        itemlist.append(Item(channel=__channel__, title="Resúmenes", action="novedades", url=scrapedurl, thumbnail=item.thumbnail, folder=True))

    return itemlist

def bbcode_kodi2html(text):
    if config.get_platform().startswith("plex") or config.get_platform().startswith("mediaserver"):
        import re
        text = re.sub(r'\[COLOR\s([^\]]+)\]',
                      r'<span style="color: \1">',
                      text)
        text = text.replace('[/COLOR]','</span>')
        text = text.replace('[CR]','<br>')
        text = re.sub(r'\[([^\]]+)\]',
                      r'<\1>',
                      text)
        text = text.replace('"color: white"','"color: auto"')

    return text